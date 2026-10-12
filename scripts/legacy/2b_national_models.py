"""Country-specific categorical WLS, BRR-Fay and ten-PV covariance.
No M3/M4/M5 fit, LDW analysis or composite AI exposure.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','2')
from common import ROOT,load_json,save_json,log
import argparse,time,json
import numpy as np
import pandas as pd
from scipy.stats import norm

AI=[f'ST438Q0{i}DA' for i in range(1,5)];DOM=['READ','MATH','SCIE']
COV=['ESCS','ST004D01T','AGE','IMMIG','ST022Q01TA']
DIG=['ST250Q02JA','ST250Q05JA','ST326Q01JA','ST326Q02JA','ST326Q04JA','ST326Q05JA','ST097Q06DA']
WEIGHTS=['W_FSTUWT']+[f'W_FSTURWT{i}' for i in range(1,81)]
CONTRASTS=['yearly_vs_never','monthly_vs_never','weekly_vs_never','daily_vs_never','daily_vs_weekly']
C=np.array([[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1],[0,0,0,-1,1]],dtype=float)
def write(df,name):df.to_csv(ROOT/'results'/name,index=False,encoding='utf-8-sig',float_format='%.12g')
def combine(theta):
    # theta has dimensions plausible value x (final+80 replicas) x coefficients.
    q=theta[:,0,:];qbar=q.mean(axis=0);delta=theta[:,1:,:]-q[:,None,:]
    U=np.einsum('mrp,mrq->pq',delta,delta)/20/10
    centered=q-qbar;B=centered.T@centered/9
    T=U+1.1*B
    return qbar,U,B,T
def stats(beta,var):
    se=float(np.sqrt(max(var,0)));p=float(2*norm.sf(abs(beta/se))) if se>0 else (1. if beta==0 else 0.)
    return {'beta':float(beta),'SE':se,'CI_low':float(beta-1.959963984540054*se),'CI_high':float(beta+1.959963984540054*se),'p':p,
            'CI95_low':float(beta-1.959963984540054*se),'CI95_high':float(beta+1.959963984540054*se),'p_raw':p}
def design(g,exposure,model,omit_sex=False):
    n=len(g);x=[np.ones(n)]+[g[exposure].eq(v).to_numpy(dtype=float) for v in [2,3,4,5]]
    terms=['intercept','AI_2','AI_3','AI_4','AI_5'];omitted=[]
    if model=='M2':
        candidates=[('ESCS',g.ESCS.to_numpy()),('male',g.ST004D01T.eq(2).to_numpy(dtype=float)),
                    ('AGE',g.AGE.to_numpy()),('IMMIG_second',g.IMMIG.eq(2).to_numpy(dtype=float)),
                    ('IMMIG_first',g.IMMIG.eq(3).to_numpy(dtype=float)),('home_other',g.ST022Q01TA.eq(2).to_numpy(dtype=float))]
        if omit_sex:candidates=[(k,v) for k,v in candidates if k!='male'];omitted.append('male: absent nationally, user authorized')
        for term,v in candidates:
            if np.ptp(v)==0:omitted.append(term+': constant in analytical sample');continue
            if term in ['ESCS','AGE']:v=v-np.average(v,weights=g.W_FSTUWT)
            x.append(v);terms.append(term)
    return np.column_stack(x),terms,omitted
def fit(g,exposure,model,domain,omit_sex=False):
    X,terms,omitted=design(g,exposure,model,omit_sex)
    Y=g[[f'PV{m}{domain}' for m in range(1,11)]].to_numpy()
    W=g[WEIGHTS].to_numpy();W=W/W.sum(axis=0)
    if np.linalg.matrix_rank(X)<X.shape[1]:return None,{'fit_status':'rank_deficient','terms':terms,'omitted':omitted}
    # Compute all 81 normal-equation systems once, solve all ten PV as RHS.
    # Chunk replicas to bound RAM for larger national samples.
    beta=[];condition=[];residual=[]
    for first in range(0,81,9):
        wr=W[:,first:first+9]
        weighted_x=wr.T[:,:,None]*X[None,:,:]
        gram=np.einsum('rni,nj->rij',weighted_x,X,optimize=True)
        rhs=np.einsum('rni,nm->rim',weighted_x,Y,optimize=True)
        cond=np.linalg.cond(gram);condition.extend(cond.tolist())
        if not np.isfinite(cond).all() or max(cond)>1e12:return None,{'fit_status':'ill_conditioned','max_condition':float(max(cond)),'terms':terms,'omitted':omitted}
        b=np.linalg.solve(gram,rhs)
        residual.append(float(np.max(np.abs(gram@b-rhs))))
        beta.append(b)
    arr=np.concatenate(beta,axis=0).transpose(2,0,1)
    return arr,{'fit_status':'estimated','terms':terms,'omitted':omitted,'max_condition':float(max(condition)),
                'normal_equation_max_abs_residual':max(residual)}
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--models',nargs='+',choices=['M0','M1','M2'],default=['M0','M1','M2'])
    parser.add_argument('--omit-national-missing-sex',action='store_true');args=parser.parse_args()
    assert load_json('results/fay2025_validation_status.json')['status']=='PASS','Fay gate not passed'
    start=time.time();cols=['CNT','CNTSTUID','OECD']+WEIGHTS+AI+COV+DIG+['ST436Q16DA']+[f'PV{i}{d}' for d in DOM for i in range(1,11)]
    data=pd.read_parquet(ROOT/'data/processed/pisa2025_ai_subset.parquet',columns=list(dict.fromkeys(cols)))
    data=data.loc[data.OECD.eq(1)].copy();meta=load_json('data/processed/stu_metadata.json')
    for v in cols:
        if v in ['CNT','CNTSTUID','OECD'] or v.startswith('W_'):continue
        for r in meta['missing_ranges'].get(v,[]):data.loc[data[v].between(r['lo'],r['hi']),v]=np.nan
    # Recompute coverage from preserved national population weights, not CSV flags.
    item_elig=[];covariates=[]
    for c,g in data.groupby('CNT'):
        total=g.W_FSTUWT.sum();row={'country':c,'weighted_N_total':total,'N_total':len(g)}
        for v in AI+['ST436Q16DA']:
            good=g[v].isin([1,2,3,4,5] if v in AI else [1,2,3,4]);row[v+'_coverage_pct']=100*g.loc[good,'W_FSTUWT'].sum()/total
        row['ST438_all_four_75_pass']=all(row[v+'_coverage_pct']>=75 for v in AI)
        row['H6_item_75_pass']=row['ST438_all_four_75_pass'] and row['ST436Q16DA_coverage_pct']>=75
        item_elig.append(row)
        for v in COV:
            covariates.append({'country':c,'covariate':v,'N_valid':int(g[v].notna().sum()),'weighted_pct_valid':100*g.loc[g[v].notna(),'W_FSTUWT'].sum()/total,
                               'nationally_absent':not g[v].notna().any()})
    eligibility=pd.DataFrame(item_elig);write(eligibility,'stage2b_country_eligibility.csv');write(pd.DataFrame(covariates),'stage2b_covariate_availability.csv')
    primary=set(eligibility.loc[eligibility.ST438_all_four_75_pass,'country'])
    h6=set(eligibility.loc[eligibility.H6_item_75_pass,'country'])
    assert set(data.CNT.unique())-primary=={'ISR','USA'}
    print('Reverified primary countries',len(primary),'H6 item-eligible',len(h6),flush=True)
    print('M2 missing-sex handling:','omit only where absent nationally' if args.omit_national_missing_sex else 'strict full specification',flush=True)
    rows={m:[] for m in args.models};coverage=[];fits=[];exploratory=[]
    covdir=ROOT/'data/processed/stage2b_model_estimates';covdir.mkdir(exist_ok=True)
    modelcols={'M1':[],'M2':COV,'M3':COV+DIG,'M5':COV+['ST436Q16DA']}
    for ci,(country,g) in enumerate(data.groupby('CNT'),1):
        total=g.W_FSTUWT.sum();nall=len(g);national_sex_absent=not g.ST004D01T.notna().any()
        omit_sex=args.omit_national_missing_sex and national_sex_absent
        for exposure in AI:
            aiok=g[exposure].isin([1,2,3,4,5]).to_numpy()
            for domain in DOM:
                Y=g[[f'PV{m}{domain}' for m in range(1,11)]].to_numpy();finite=np.isfinite(Y)
                assert (finite==finite[:,[0]]).all(),'PV-specific missing patterns need separate treatment'
                outcome=finite.all(axis=1);aiout=aiok&outcome
                masks={}
                for model,required in modelcols.items():
                    required=[v for v in required if not (omit_sex and v=='ST004D01T')]
                    mask=aiout&g[required].notna().all(axis=1).to_numpy() if required else aiout
                    masks[model]=mask;nn=int(mask.sum());ww=float(g.loc[mask,'W_FSTUWT'].sum());pct=100*ww/total
                    base_ok=country in (h6 if model=='M5' else primary)
                    coverage.append({'country':country,'exposure':exposure,'domain':domain,'model':model,'N_total':nall,'weighted_N_total':total,
                        'N':nn,'weighted_N':ww,'joint_linkage_pct':pct,'joint_coverage_pct':pct,'below_75_joint_coverage':pct<75,
                        'country_item_eligible':base_ok,'primary_synthesis_eligible':base_ok and pct>=75,'fit_authorized_this_stage':model in ['M1','M2'],
                        'coverage_only_prospective':model in ['M3','M5'],'required_variables':','.join([exposure]+required+[f'PV1–10{domain}']),
                        'M2_sex_omitted_nationally':omit_sex,'specification_note':'M3=M2+digital controls; M5=M2+critical interaction candidate; no M3/M5 fitted'})
                if 'M0' in args.models:
                    denom=float(g.loc[aiout,'W_FSTUWT'].sum())
                    for cat in range(1,6):
                        sub=g.loc[aiout&g[exposure].eq(cat).to_numpy()];w=sub[WEIGHTS].to_numpy()
                        means=w.T@sub[[f'PV{m}{domain}' for m in range(1,11)]].to_numpy()/w.sum(axis=0)[:,None]
                        theta=means.T[:,:,None];q,u,b,t=combine(theta)
                        row={'country':country,'exposure':exposure,'domain':domain,'category':cat,'N':len(sub),'weighted_N':sub.W_FSTUWT.sum(),
                             'frequency_pct_among_valid_exposure_outcome':100*sub.W_FSTUWT.sum()/denom,'coverage_pct':100*denom/total,
                             'country_item_eligible':country in primary,'scope':'primary_candidate' if country in primary else 'low_coverage_exploratory',
                             'mean_PISA':q[0],'SE':np.sqrt(t[0,0]),'CI_low':q[0]-1.959963984540054*np.sqrt(t[0,0]),'CI_high':q[0]+1.959963984540054*np.sqrt(t[0,0]),
                             'sampling_variance':u[0,0],'between_PV_variance':b[0,0]}
                        rows['M0'].append(row)
                for model in [m for m in args.models if m in ['M1','M2']]:
                    mask=masks[model];sub=g.loc[mask];nn=len(sub);ww=float(sub.W_FSTUWT.sum());pct=100*ww/total
                    base={'country':country,'exposure':exposure,'domain':domain,'model':model,'N':nn,'weighted_N':ww,
                          'joint_coverage_pct':pct,'joint_linkage_pct':pct,'coverage':pct,'below_75_joint_coverage':pct<75,
                          'country_item_eligible':country in primary,'primary_synthesis_eligible':country in primary and pct>=75,
                          'M2_sex_omitted_nationally':omit_sex,'N_total':nall,'weighted_N_total':total}
                    info={'fit_status':'no_complete_cases','terms':[],'omitted':[]};theta=None
                    if nn>0:theta,info=fit(sub,exposure,model,domain,omit_sex)
                    fits.append({**base,**info,'terms':json.dumps(info['terms']),'omitted':json.dumps(info['omitted'])})
                    if theta is not None:
                        # Save exposure/intercept arrays to reconstruct arbitrary
                        # contrasts/covariance, retaining correlated rep/PV labels.
                        np.savez_compressed(covdir/f'{country}_{exposure}_{domain}_{model}.npz',theta=theta[:,:,:5])
                        ct=np.einsum('mrp,cp->mrc',theta[:,:,:5],C);q,U,B,T=combine(ct)
                        for j,contrast in enumerate(CONTRASTS):
                            row={**base,'contrast':contrast,**stats(q[j],T[j,j]),'sampling_variance':U[j,j],
                                 'between_PV_variance':B[j,j],'total_variance':T[j,j],
                                 'fit_status':'estimated','controls_omitted':';'.join(info['omitted'])}
                            (rows[model] if country in primary else exploratory).append(row)
                    else:
                        for contrast in CONTRASTS:
                            row={**base,'contrast':contrast,'beta':np.nan,'SE':np.nan,'CI_low':np.nan,'CI_high':np.nan,'p':np.nan,
                                 'CI95_low':np.nan,'CI95_high':np.nan,'p_raw':np.nan,'fit_status':info['fit_status'],'controls_omitted':';'.join(info['omitted'])}
                            (rows[model] if country in primary else exploratory).append(row)
        print(f'{ci}/38 {country}: completed '+','.join(args.models)+f'; elapsed {time.time()-start:.1f}s',flush=True)
        for model,items in rows.items():
            if items:write(pd.DataFrame(items),'descriptives_M0.csv' if model=='M0' else f'country_effects_{model}.csv')
    write(pd.DataFrame(coverage),'model_joint_coverage.csv')
    fitpath=ROOT/'results/national_fit_diagnostics.csv'
    if fitpath.exists():
        old=pd.read_csv(fitpath);old=old.loc[~old.model.isin(args.models)];fits=pd.concat([old,pd.DataFrame(fits)],ignore_index=True)
    else:fits=pd.DataFrame(fits)
    write(fits,'national_fit_diagnostics.csv')
    exppath=ROOT/'results/low_coverage_exploratory_ISR_USA.csv'
    if exppath.exists():
        old=pd.read_csv(exppath);old=old.loc[~old.model.isin(args.models)];exploratory=pd.concat([old,pd.DataFrame(exploratory)],ignore_index=True)
    else:exploratory=pd.DataFrame(exploratory)
    exploratory['exploratory_only']=True;exploratory['insufficient_item_coverage']=True
    write(exploratory,'low_coverage_exploratory_ISR_USA.csv')
    save_json('results/stage2b_national_run.json',{'models_this_run':args.models,'M2_sex_handling':'national missing sex omitted by explicit authorization' if args.omit_national_missing_sex else 'strict complete specification',
        'main_country_codes':sorted(primary),'main_country_K':len(primary),'H6_item_country_codes':sorted(h6),'H6_item_K':len(h6),
        'elapsed_seconds':time.time()-start,'fit_M3_M4_M5_LDW':False})
    log('Modelos nacionales '+','.join(args.models),f'{len(primary)} candidatos principales; {len(h6)} candidatos H6; {time.time()-start:.1f}s',
        'Media OCDE posterior solo con países que pasan cobertura conjunta; ISR/USA apéndice; conservar no estimables')

if __name__=='__main__':main()
