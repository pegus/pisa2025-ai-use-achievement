"""Ordinal dependence, cell support, antecedent profiles and ecology."""
import os
os.environ['OPENBLAS_NUM_THREADS']='2'
from common import ROOT,load_json,log
import pandas as pd,numpy as np,itertools
from scipy.stats import norm
from importlib.util import spec_from_file_location,module_from_spec
sp=spec_from_file_location('models',ROOT/'scripts/2c_models.py');models=module_from_spec(sp);sp.loader.exec_module(models)
AI=models.AI;WEIGHTS=models.WEIGHTS
def write(df,name):models.write(df,name)
def ordinal_rho(table):
    p=table/table.sum();pa=p.sum(axis=1);pb=p.sum(axis=0)
    ra=np.cumsum(pa)-pa/2;rb=np.cumsum(pb)-pb/2
    ma=pa@ra;mb=pb@rb
    cov=np.sum(p*(ra[:,None]-ma)*(rb[None,:]-mb));va=pa@((ra-ma)**2);vb=pb@((rb-mb)**2)
    return cov/np.sqrt(va*vb) if va*vb>0 else np.nan
def main():
    data=pd.read_parquet(ROOT/'data/processed/pisa2025_stage2c_oecd.parquet');spec=load_json('results/stage2c_specification.json')
    corr=[];cells=[];profiles=[];reverse=[];ecology=[];pooled={pair:[] for pair in itertools.combinations(AI,2)}
    temporal={ 'ST127Q01TA':'primary-school history: plausibly earlier but onset of AI unobserved',
      'ST127Q02TA':'lower-secondary history: ordering versus AI onset unknown',
      'ST127Q03TA':'upper-secondary history: ordering versus AI onset unknown',
      'ST062Q01TA':'past two weeks: concurrent; NOT a pre-exposure control',
      'ST062Q02TA':'past two weeks: concurrent; NOT a pre-exposure control',
      'ST062Q03TA':'past two weeks: concurrent; NOT a pre-exposure control'}
    for country,g in data.loc[data.CNT.isin(spec['candidate_countries'])].groupby('CNT'):
        total=g.W_FSTUWT.sum()
        for a,b in itertools.combinations(AI,2):
            sub=g.loc[g[a].isin(range(1,6))&g[b].isin(range(1,6))]
            indexes=(sub[a].to_numpy(int)-1)*5+sub[b].to_numpy(int)-1
            W=sub[WEIGHTS].to_numpy();tables=np.stack([np.bincount(indexes,weights=W[:,r],minlength=25).reshape(5,5) for r in range(81)])
            rhos=np.array([ordinal_rho(t) for t in tables]);var=np.sum((rhos[1:]-rhos[0])**2)/20
            corr.append({'country':country,'exposure_A':a,'exposure_B':b,'statistic':'weighted_midrank_Spearman',
               'rho':rhos[0],'SE':np.sqrt(var),'N':len(sub),'weighted_N':W[:,0].sum(),'joint_coverage_pct':100*W[:,0].sum()/total,
               'scope':'national','K':1,'method':'weighted CDF midranks recomputed for each replica; no PISA PV involved'})
            pooled[(a,b)].append(tables[0]/tables[0].sum())
            counts=np.bincount(indexes,minlength=25).reshape(5,5)
            for i,j in itertools.product(range(5),repeat=2):cells.append({'country':country,'exposure_A':a,'exposure_B':b,
               'category_A':i+1,'category_B':j+1,'N':counts[i,j],'weighted_N':tables[0,i,j],'N_lt_10':counts[i,j]<10,'zero_cell':counts[i,j]==0})
        joint=g.loc[g[AI].isin(range(1,6)).all(axis=1)];idx=((joint[AI].to_numpy(int)-1)*np.array([125,25,5,1])).sum(axis=1)
        counts=np.bincount(idx,minlength=625);weights=np.bincount(idx,weights=joint.W_FSTUWT,minlength=625)
        for i,cats in enumerate(itertools.product(range(1,6),repeat=4)):
            profiles.append({'country':country,**dict(zip(AI,cats)),'N':counts[i],'weighted_N':weights[i],'N_lt_10':counts[i]<10,'zero_profile':counts[i]==0})
        for exposure in AI:
            for history,timing in temporal.items():
                sub=g.loc[g[exposure].isin(range(1,6))&g[history].isin(range(1,5) if history.startswith('ST062') else range(1,4))]
                W=sub[WEIGHTS].to_numpy();event=sub[history].gt(1).to_numpy(float)
                ratios={};sample={}
                for cat in range(1,6):
                    sel=sub[exposure].eq(cat).to_numpy();w=W[sel];y=event[sel];den=w.sum(axis=0)
                    prop=(w.T@y)/den if len(w) else np.full(81,np.nan);ratios[cat]=prop;sample[cat]=(len(w),den[0] if len(w) else 0)
                    var=np.sum((prop[1:]-prop[0])**2)/20
                    reverse.append({'country':country,'exposure':exposure,'diagnostic':history,'group':f'category_{cat}',
                       'statistic':'event_prevalence','estimate':prop[0],'SE':np.sqrt(var),'N':sample[cat][0],'weighted_N':sample[cat][1],
                       'joint_coverage_pct':100*sub.W_FSTUWT.sum()/total,'temporal_status':timing,'event_definition':'response >1',
                       'causal_correction':False})
                delta=ratios[5]-ratios[1];var=np.sum((delta[1:]-delta[0])**2)/20
                reverse.append({'country':country,'exposure':exposure,'diagnostic':history,'group':'daily_minus_never',
                    'statistic':'prevalence_difference','estimate':delta[0],'SE':np.sqrt(var),'p_raw':2*norm.sf(abs(delta[0])/np.sqrt(var)) if var>0 else np.nan,
                    'N':sum(sample[c][0] for c in [1,5]),'weighted_N':sum(sample[c][1] for c in [1,5]),
                    'joint_coverage_pct':100*sub.W_FSTUWT.sum()/total,'temporal_status':timing,'event_definition':'response >1','causal_correction':False})
            good=g[exposure].isin(range(1,6));sub=g.loc[good];w=sub.W_FSTUWT
            row={'country':country,'exposure':exposure,'coverage_pct':100*w.sum()/total,
               'AI_any_pct':100*w.loc[sub[exposure].gt(1)].sum()/w.sum(),'AI_daily_pct':100*w.loc[sub[exposure].eq(5)].sum()/w.sum()}
            valid=g.ESCS.notna();row['ESCS_mean']=np.average(g.loc[valid,'ESCS'],weights=g.loc[valid,'W_FSTUWT']) if valid.any() else np.nan
            for domain in models.DOM:
                y=g[[f'PV{m}{domain}' for m in range(1,11)]].to_numpy();sel=np.isfinite(y).all(axis=1)
                row[f'national_mean_{domain}']=np.average(y[sel],axis=0,weights=g.loc[sel,'W_FSTUWT']).mean()
                row[f'national_SD_{domain}']=np.sqrt(np.mean([np.average((y[sel,i]-np.average(y[sel,i],weights=g.loc[sel,'W_FSTUWT']))**2,weights=g.loc[sel,'W_FSTUWT']) for i in range(10)]))
            ecology.append(row)
    c=pd.DataFrame(corr)
    for (a,b),tables in pooled.items():
        nations=c.loc[c.exposure_A.eq(a)&c.exposure_B.eq(b)];K=len(nations)
        corr.append({'country':'OECD_EQUAL_COUNTRY','exposure_A':a,'exposure_B':b,'statistic':'mean_national_weighted_Spearman',
            'rho':nations.rho.mean(),'SE':np.sqrt((nations.SE**2).sum())/K,'N':nations.N.sum(),'K':K,'scope':'global_descriptive',
            'method':'equal mean of national correlations; independent national sampling variances'})
        corr.append({'country':'OECD_POOLED_EQUAL_COUNTRY','exposure_A':a,'exposure_B':b,'statistic':'pooled_weighted_midrank_Spearman',
            'rho':ordinal_rho(np.sum(tables,axis=0)),'SE':np.nan,'N':nations.N.sum(),'K':K,'scope':'global_descriptive',
            'method':'pair-complete respondents renormalized equally by country; pooled covariance includes ecological component; no joint replica assumption'})
    write(pd.DataFrame(corr),'AI_use_correlations.csv');write(pd.DataFrame(cells),'joint_AI_pairwise_cells.csv');write(pd.DataFrame(profiles),'joint_AI_profile_support.csv')
    write(pd.DataFrame(reverse),'reverse_causality_diagnostics.csv');write(pd.DataFrame(ecology),'stage2c_country_characteristics.csv')
    log('Diagnósticos 2C','Correlaciones ordinales, celdas, repetición/ausencia y perfiles nacionales','Comparison controls no equivalen a negative controls validados')
    print('Descriptive diagnostics complete',flush=True)
if __name__=='__main__':main()
