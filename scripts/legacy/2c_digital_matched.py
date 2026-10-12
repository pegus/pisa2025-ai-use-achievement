"""Digital comparison and all four separate AI fits on exactly the same cases."""
import os
os.environ['OPENBLAS_NUM_THREADS']='2'
from common import ROOT,load_json,log
import numpy as np,pandas as pd,time
from importlib.util import spec_from_file_location,module_from_spec
sp=spec_from_file_location('models',ROOT/'scripts/2c_models.py');m=module_from_spec(sp);sp.loader.exec_module(m)
def main():
    data=pd.read_parquet(ROOT/'data/processed/pisa2025_stage2c_oecd.parquet');spec=load_json('results/stage2c_specification.json')
    rows=[];start=time.time()
    for i,country in enumerate(spec['candidate_countries'],1):
        g=data.loc[data.CNT.eq(country)];total=g.W_FSTUWT.sum()
        for digital in spec['digital_comparison_exposures']:
            mask=m.make_mask(g,m.AI+[digital],m.CORE)
            if digital.startswith('ST322'):mask=mask & g[digital].isin(range(1,6)).to_numpy()
            sub=g.loc[mask];coverage=100*sub.W_FSTUWT.sum()/total
            for exposure in [digital]+m.AI:
                common={'country':country,'digital_comparator':digital,'exposure':exposure,'base_controls':'CORE','N':len(sub),
                    'weighted_N':sub.W_FSTUWT.sum(),'joint_coverage_pct':coverage,'coverage_75_pass':coverage>=75,'same_students_for_AI_and_digital':True,
                    'not_validated_negative_control':True}
                info={'fit_status':'no_complete_cases'};theta=None
                if len(sub)>0 and min(sub[exposure].eq(k).sum() for k in range(1,6))>=30:
                    X,terms,omitted=m.design(sub,[exposure],m.CORE);theta,info=m.fit_arrays(sub,X,terms)
                elif len(sub)>0:info={'fit_status':'insufficient_support_predefined'}
                if theta is not None:
                    selected=theta[:,:,:,[terms.index(f'{exposure}_{k}') for k in range(2,6)]]
                    np.savez_compressed(m.SAVE/f'{country}__DIGITAL-MATCHED__CORE__{digital}__{exposure}.npz',theta=selected)
                    labels=m.CONTRASTS if exposure in m.AI else (
                        ['monthly_vs_never','weekly_vs_never','daily_vs_never','several_times_daily_vs_never','several_times_daily_vs_daily'] if digital.startswith('IC171') else
                        ['less_than_half_vs_never','half_vs_never','more_than_half_vs_never','all_time_vs_never','all_time_vs_more_than_half'])
                    for di,d in enumerate(m.DOM):
                        a=selected[di];ct=np.concatenate([a,(a[:,:,3]-a[:,:,2])[:,:,None]],axis=2);q,U,B,T=m.combine(ct)
                        for j,label in enumerate(labels):rows.append({**common,'domain':d,'contrast':label,**m.stats(q[j],T[j,j]),
                             'sampling_variance':U[j,j],'between_PV_variance':B[j,j],'fit_status':'estimated','primary_synthesis_eligible':coverage>=75})
                else:
                    for d in m.DOM:rows.append({**common,'domain':d,'contrast':'not_estimable','beta':np.nan,'SE':np.nan,'p_raw':np.nan,
                        'fit_status':info['fit_status'],'primary_synthesis_eligible':False})
        if i%6==0:print(f'Digital matched {i}/36, {time.time()-start:.1f}s',flush=True)
    m.write(pd.DataFrame(rows),'digital_comparison_same_sample.csv')
    log('Comparadores digitales misma muestra','IA y comportamiento digital ajustados con CORE sobre los mismos estudiantes','No presentar negative controls causales ni combinar diseños internacionales')
if __name__=='__main__':main()
