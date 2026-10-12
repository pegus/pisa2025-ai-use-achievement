"""National WLS and weighted school absorption for all 10 PV and 81 weights.
Never average student plausible values before fitting. No LDW.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='2'
from common import ROOT,load_json,save_json,log
import numpy as np,pandas as pd,time,json,argparse
from scipy.sparse import csr_matrix
from importlib.util import spec_from_file_location,module_from_spec
sp=spec_from_file_location('bmodels',ROOT/'scripts/2b_national_models.py');bmodels=module_from_spec(sp);sp.loader.exec_module(bmodels)
AI=bmodels.AI;DOM=bmodels.DOM;CONTRASTS=bmodels.CONTRASTS;WEIGHTS=bmodels.WEIGHTS;combine=bmodels.combine;stats=bmodels.stats
CORE=['ESCS','IMMIG','ST022Q01TA'];FULL=['ESCS','ST004D01T','AGE','IMMIG','ST022Q01TA']
ACCESS=['ST250Q02JA','ST250Q05JA'];AMBIG=['ST326Q01JA','ST326Q02JA','ST326Q04JA','ST326Q05JA','ST097Q06DA']
SAVE=ROOT/'data/processed/stage2c_model_estimates';SAVE.mkdir(exist_ok=True)
def write(df,name):df.to_csv(ROOT/'results'/name,index=False,encoding='utf-8-sig',float_format='%.12g')
def Ycols():return [f'PV{m}{d}' for d in DOM for m in range(1,11)]
def make_mask(g,exposures,controls,school=False):
    req=list(dict.fromkeys(exposures+controls+Ycols()+(['CNTSCHID'] if school else [])))
    return g[req].notna().all(axis=1).to_numpy()
def design(g,exposures,controls,school=False):
    x=[] if school else [np.ones(len(g))];terms=[] if school else ['intercept'];omitted=[]
    for v in exposures:
        cats=list(range(2,6)) if v in AI else (list(range(2,7)) if v.startswith('IC171') else list(range(2,6)))
        for k in cats:x.append(g[v].eq(k).to_numpy(float));terms.append(f'{v}_{k}')
    for v in controls:
        if v in ['ESCS','AGE']:
            a=g[v].to_numpy(float);a=a-np.average(a,weights=g.W_FSTUWT);candidates=[(v,a)]
        else:
            values={'IMMIG':[2,3],'ST004D01T':[2],'ST022Q01TA':[2],'ST250Q02JA':[2],'ST250Q05JA':[2],
                    'ST097Q06DA':[2,3,4],'ST127Q01TA':[2,3]}.get(v,list(range(2,10)) if v.startswith('ST326') else sorted(g[v].unique())[1:])
            candidates=[(f'{v}_{k}',g[v].eq(k).to_numpy(float)) for k in values]
        for term,a in candidates:
            if np.ptp(a)==0:omitted.append(term+':constant');continue
            x.append(a);terms.append(term)
    return np.column_stack(x),terms,omitted
def fit_arrays(g,X,terms,school=False):
    Y=g[Ycols()].to_numpy(float);W=g[WEIGHTS].to_numpy(float);W=W/W.sum(axis=0)
    rank=np.linalg.matrix_rank(X)
    if rank<X.shape[1]:return None,{'fit_status':'rank_deficient','rank':rank}
    conds=[];beta=[];removed=[]
    if school:
        codes,schools=pd.factorize(g.CNTSCHID,sort=True);s=len(schools)
        Z=csr_matrix((np.ones(len(g)),(codes,np.arange(len(g)))),shape=(s,len(g)))
        for r in range(81):
            w=W[:,r];wx=w[:,None]*X;wy=w[:,None]*Y
            sw=np.asarray(Z@w);sx=np.asarray(Z@wx);sy=np.asarray(Z@wy)
            inv=np.divide(1,sw,out=np.zeros_like(sw),where=sw>0)
            # Schur complement equals separately weighted within transformation
            # for this replicate and each of the thirty outcome/PV columns.
            gram=X.T@wx-sx.T@(sx*inv[:,None]);rhs=X.T@wy-sx.T@(sy*inv[:,None])
            gram=(gram+gram.T)/2
            if r==0:
                keep=np.diag(gram)>1e-11
                removed=[terms[i]+':no within-school variation' for i in np.flatnonzero(~keep)]
                if not keep[:4].all():return None,{'fit_status':'AI_not_identified_within_school','removed_within':removed}
            gram=gram[np.ix_(keep,keep)];rhs=rhs[keep]
            cond=float(np.linalg.cond(gram));conds.append(cond)
            if not np.isfinite(cond) or cond>1e12:return None,{'fit_status':'ill_conditioned_replica','max_gram_condition':cond,'failed_replica':r}
            small=np.linalg.solve(gram,rhs);out=np.zeros((len(terms),30));out[keep]=small;beta.append(out)
        arr=np.stack(beta)
    else:
        for first in range(0,81,9):
            wr=W[:,first:first+9];wx=wr.T[:,:,None]*X[None,:,:]
            gram=np.einsum('rni,nj->rij',wx,X,optimize=True);rhs=np.einsum('rni,nm->rim',wx,Y,optimize=True)
            cond=np.linalg.cond(gram);conds.extend(cond.tolist())
            if not np.isfinite(cond).all() or max(cond)>1e12:return None,{'fit_status':'ill_conditioned_replica','max_gram_condition':float(max(cond))}
            beta.append(np.linalg.solve(gram,rhs))
        arr=np.concatenate(beta)
    theta=arr.transpose(2,0,1).reshape(3,10,81,len(terms))
    # Proper weighted-design condition and VIF, removing intercept for correlation.
    ai_idx=[i for i,t in enumerate(terms) if any(t.startswith(v+'_') for v in AI)]
    xx=X if school else X[:,1:]
    if not school:
        w=W[:,0];center=xx-np.sum(w[:,None]*xx,axis=0);cov=center.T@(w[:,None]*center)
        sd=np.sqrt(np.diag(cov));corr=cov/sd[:,None]/sd[None,:]
        standardized_condition=float(np.sqrt(np.linalg.cond(corr)))
        vifs=np.diag(np.linalg.inv(corr));ai_vif=float(max(vifs[i-1] for i in ai_idx)) if ai_idx else np.nan
        vif_terms=json.dumps({terms[i+1]:float(v) for i,v in enumerate(vifs)})
    else:standardized_condition=ai_vif=np.nan;vif_terms='{}'
    return theta,{'fit_status':'estimated','max_gram_condition':max(conds),'standardized_design_condition':standardized_condition,
                   'max_AI_dummy_VIF':ai_vif,'VIF_terms':vif_terms,'removed_within':';'.join(removed)}
def support(g,country,exposure,base,allweight):
    records=[]
    for school,h in g.groupby('CNTSCHID'):
        w=h.W_FSTUWT.to_numpy();a=h[exposure].to_numpy();avg=np.average(a,weights=w)
        row={'country':country,'exposure':exposure,'base_controls':base,'CNTSCHID':school,'N':len(h),'weighted_N':w.sum(),
             'N_categories':len(np.unique(a)),'informative_school':len(np.unique(a))>1,'weighted_ordinal_variance':np.average((a-avg)**2,weights=w)}
        for k in range(1,6):row[f'N_category_{k}']=int((a==k).sum());row[f'weighted_N_category_{k}']=float(w[a==k].sum())
        records.append(row)
    d=pd.DataFrame(records);counts={f'N_category_{k}':int(g[exposure].eq(k).sum()) for k in range(1,6)}
    informative=d.informative_school if len(d) else pd.Series([],dtype=bool)
    result={'country':country,'exposure':exposure,'base_controls':base,'N':len(g),'weighted_N':g.W_FSTUWT.sum(),
       'joint_coverage_pct':100*g.W_FSTUWT.sum()/allweight,'N_schools':len(d),'N_informative_schools':int(informative.sum()),
       'N_noninformative_schools':int((~informative).sum()),'N_in_informative_schools':int(d.loc[informative,'N'].sum()) if len(d) else 0,
       'weighted_pct_in_informative_schools':100*d.loc[informative,'weighted_N'].sum()/g.W_FSTUWT.sum() if len(g) else np.nan,
       'support_pass':len(d)>0 and informative.sum()>=30 and min(counts.values())>=30,**counts}
    for k in range(1,6):
        result[f'N_schools_with_category_{k}']=int((d[f'N_category_{k}']>0).sum()) if len(d) else 0
        result[f'N_schools_with_category_{k}_and_never']=int(((d[f'N_category_{k}']>0)&(d.N_category_1>0)).sum()) if len(d) else 0
    return result,records
def run_country(country,g,spec):
    rows=[];diagnostics=[];schools=[];schoolagg=[]
    total=float(g.W_FSTUWT.sum());full21=spec['full21']
    def run(model,exposures,controls,mask,school=False,base='CORE',minimum_support=True):
        sub=g.loc[mask];N=len(sub);weight=float(sub.W_FSTUWT.sum());coverage=100*weight/total
        common={'country':country,'model':model,'base_controls':base,'N':N,'weighted_N':weight,'N_total':len(g),'weighted_N_total':total,
                'joint_coverage_pct':coverage,'coverage_75_pass':coverage>=75,'joint_coverage_75_pass':coverage>=75,'country_item_eligible':True}
        info={'fit_status':'no_complete_cases'};theta=None;terms=[];omitted=[];categories=[]
        for v in exposures:
            for k in range(1,6):
                z=sub.loc[sub[v].eq(k),'W_FSTUWT'].to_numpy();neff=z.sum()**2/(z@z) if len(z) else 0
                categories.append({'exposure':v,'category':k,'N':len(z),'n_eff_Kish':neff})
        category_ok=bool(N and min(x['N'] for x in categories)>=30)
        effective_ok=bool(N and min(x['n_eff_Kish'] for x in categories)>=10)
        if N and minimum_support and category_ok:
            X,terms,omitted=design(sub,exposures,controls,school)
            theta,info=fit_arrays(sub,X,terms,school)
        elif N:info={'fit_status':'insufficient_support_predefined'}
        isjoint=len(exposures)==4
        interpret=theta is not None and (not isjoint or (effective_ok and info['max_AI_dummy_VIF']<=10 and info['standardized_design_condition']<=30))
        info.update({'category_support_pass':category_ok,'effective_N_support_pass':effective_ok,'interpretability_pass':interpret,
                    'category_counts':json.dumps(categories),'terms':json.dumps(terms),'controls_omitted':';'.join(omitted)})
        diagnostics.append({**common,'exposures':';'.join(exposures),'school_fixed_effects':school,**info})
        if theta is not None:
            # Store only exposure coefficients: no individual records.
            indices=[[terms.index(f'{v}_{k}') for k in range(2,6)] for v in exposures]
            selected=theta[:,:,:,np.ravel(indices)].reshape(3,10,81,len(exposures),4)
            np.savez_compressed(SAVE/f'{country}__{model}__{base}__{"JOINT" if isjoint else exposures[0]}.npz',theta=selected,
                                N=N,weighted_N=weight,coverage=coverage,exposures=np.array(exposures),interpretability=interpret)
            for ei,v in enumerate(exposures):
                for di,domain in enumerate(DOM):
                    arr=selected[di,:,:,ei,:];ct=np.concatenate([arr,(arr[:,:,3]-arr[:,:,2])[:,:,None]],axis=2)
                    q,U,B,T=combine(ct)
                    for j,contrast in enumerate(CONTRASTS):
                        rows.append({**common,'exposure':v,'domain':domain,'contrast':contrast,**stats(q[j],T[j,j]),
                             'sampling_variance':U[j,j],'between_PV_variance':B[j,j],'total_variance':T[j,j],
                             'fit_status':info['fit_status'],'interpretability_pass':interpret,
                             'primary_synthesis_eligible':coverage>=75 and interpret,'max_AI_dummy_VIF':info.get('max_AI_dummy_VIF',np.nan),
                             'standardized_design_condition':info.get('standardized_design_condition',np.nan),'controls_omitted':info['controls_omitted']})
        else:
            for v in exposures:
                for domain in DOM:
                    for contrast in CONTRASTS:rows.append({**common,'exposure':v,'domain':domain,'contrast':contrast,
                      'beta':np.nan,'SE':np.nan,'p_raw':np.nan,'CI95_low':np.nan,'CI95_high':np.nan,'sampling_variance':np.nan,
                      'between_PV_variance':np.nan,'total_variance':np.nan,'fit_status':info['fit_status'],
                      'interpretability_pass':False,'primary_synthesis_eligible':False})
    for exposure in AI:
        mcore=make_mask(g,[exposure],CORE);mfull=make_mask(g,[exposure],FULL)
        run('M2-CORE',[exposure],CORE,mcore)
        run('M1-CORE-SAMPLE',[exposure],[],mcore)
        run('M2-FULL',[exposure],FULL,mfull,base='FULL')
        if country in full21:
            run('M1-FULL-SAMPLE',[exposure],[],mfull,base='FULL')
            run('M2-CORE-FULL-SAMPLE',[exposure],CORE,mfull)
        for base,controls in [('CORE',CORE),('FULL',FULL)]:
            if base=='FULL' and country not in full21:continue
            mschool=make_mask(g,[exposure],controls,True)
            spass,sdetail=support(g.loc[mschool],country,exposure,base,total);schoolagg.append(spass);schools.extend(sdetail)
            run('M2-SCHOOL-FE',[exposure],controls,mschool,True,base,spass['support_pass'])
            # Same school-ID sample for the non-FE comparator, if IDs are missing.
            run('M2-NO-FE-SAME-SAMPLE',[exposure],controls,mschool,base=base)
            for model,digital in [('M3-CONFOUNDERS',ACCESS),('M3-INCLUDING-POTENTIAL-MEDIATORS',ACCESS+AMBIG)]:
                mdigital=make_mask(g,[exposure],controls+digital)
                run(model,[exposure],controls+digital,mdigital,base=base)
                run('M2-SAME-SAMPLE-'+model,[exposure],controls,mdigital,base=base)
        # Primary-school repetition: diagnostic sensitivity, not reverse-causality correction.
        mrepeat=make_mask(g,[exposure],CORE+['ST127Q01TA'])
        run('M2-CORE-PRIMARY-REPETITION',[exposure],CORE+['ST127Q01TA'],mrepeat)
        run('M2-CORE-REPETITION-SAMPLE',[exposure],CORE,mrepeat)
    for base,controls in [('CORE',CORE),('FULL',FULL)]:
        if base=='FULL' and country not in full21:continue
        joint=make_mask(g,AI,controls)
        run('JOINT-AI-USES',AI,controls,joint,base=base)
        for exposure in AI:run('SEPARATE-AI-JOINT-SAMPLE',[exposure],controls,joint,base=base)
    for exposure in spec['digital_comparison_exposures']:
        mask=make_mask(g,[exposure],CORE)
        # IC171 category6 is valid unavailability, not frequency; separate dummy.
        # ST322 category6=not applicable must not be an ordered exposure.
        if exposure.startswith('ST322'):mask=mask & g[exposure].isin(range(1,6)).to_numpy()
        run('DIGITAL-COMPARISON',[exposure],CORE,mask)
    return rows,diagnostics,schoolagg,schools
def main():
    start=time.time();assert load_json('results/fay2025_validation_status.json')['status']=='PASS'
    data=pd.read_parquet(ROOT/'data/processed/pisa2025_stage2c_oecd.parquet');spec=load_json('results/stage2c_specification.json')
    allrows=[];allfits=[];supportrows=[];schoolrows=[]
    for i,country in enumerate(spec['candidate_countries'],1):
        rows,fits,supports,detail=run_country(country,data.loc[data.CNT.eq(country)],spec)
        allrows.extend(rows);allfits.extend(fits);supportrows.extend(supports);schoolrows.extend(detail)
        print(f'{i}/36 {country} complete; {time.time()-start:.1f}s; {sum(r["fit_status"]=="estimated" for r in fits)}/{len(fits)} fits',flush=True)
        write(pd.DataFrame(allfits),'stage2c_fit_diagnostics.csv')
        write(pd.DataFrame(allrows),'stage2c_all_national_models.csv')
    df=pd.DataFrame(allrows)
    for prefix,mapping in [('IC171',dict(zip(CONTRASTS,['monthly_vs_never','weekly_vs_never','daily_vs_never','several_times_daily_vs_never','several_times_daily_vs_daily']))),
                           ('ST322',dict(zip(CONTRASTS,['less_than_half_vs_never','half_vs_never','more_than_half_vs_never','all_time_vs_never','all_time_vs_more_than_half'])))]:
        ix=df.model.eq('DIGITAL-COMPARISON') & df.exposure.str.startswith(prefix)
        df.loc[ix,'contrast']=df.loc[ix,'contrast'].map(mapping)
    write(df,'stage2c_all_national_models.csv')
    filenames={'M2-CORE':'M2_core_results.csv','M2-SCHOOL-FE':'school_FE_results.csv','JOINT-AI-USES':'joint_AI_uses_model.csv','DIGITAL-COMPARISON':'digital_comparison_controls.csv'}
    for model,file in filenames.items():write(df.loc[df.model.eq(model)],file)
    write(df.loc[df.model.isin(['M3-CONFOUNDERS','M3-INCLUDING-POTENTIAL-MEDIATORS'])],'M3_results.csv')
    write(pd.DataFrame(supportrows),'school_FE_support.csv');write(pd.DataFrame(schoolrows),'school_FE_support_by_school.csv')
    # Full-model reproduction is a numerical check, never a change to stage 2B.
    old=pd.read_csv(ROOT/'results/country_effects_M2.csv');old=old.loc[old.fit_status.eq('estimated')&old.primary_synthesis_eligible]
    new=df.loc[df.model.eq('M2-FULL')&df.primary_synthesis_eligible]
    compared=old.merge(new,on=['country','exposure','domain','contrast'],suffixes=('_2b','_2c'),validate='one_to_one')
    assert len(compared)==1260
    compared['abs_beta_difference']=abs(compared.beta_2b-compared.beta_2c);compared['abs_SE_difference']=abs(compared.SE_2b-compared.SE_2c)
    assert compared.abs_beta_difference.max()<1e-8 and compared.abs_SE_difference.max()<1e-8
    write(compared[['country','exposure','domain','contrast','beta_2b','beta_2c','SE_2b','SE_2c','abs_beta_difference','abs_SE_difference']],'M2_full_reproduction.csv')
    save_json('results/stage2c_national_run.json',{'elapsed_seconds':time.time()-start,'max_M2_full_beta_difference':compared.abs_beta_difference.max(),
       'max_M2_full_SE_difference':compared.abs_SE_difference.max(),'full21_exact_numerical_reproduction':True,'national_rows':len(df),'LDW':False})
    log('Modelos nacionales 2C','CORE/FULL/FE/M3/conjunto y comparadores con 10 PV x 81 pesos','Síntesis posterior solo con cobertura/soporte predefinidos')
if __name__=='__main__':main()
