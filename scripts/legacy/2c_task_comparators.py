"""Questionnaire-selected comparison tasks: browsing, sharing and production.
Selection is based on wording; no coefficient-dependent selection.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='2'
from common import ROOT,load_json,log
import numpy as np,pandas as pd,pyreadstat,time
from importlib.util import spec_from_file_location,module_from_spec
sp=spec_from_file_location('models',ROOT/'scripts/2c_models.py');m=module_from_spec(sp);sp.loader.exec_module(m)
NEW=['IC176Q02JA','IC176Q05JA','IC177Q07JA']
def main():
    start=time.time();extra,_=pyreadstat.read_sav(str(ROOT.parent/'work/raw/CY09_MS_STU_PUF.sav'),usecols=['CNT','CNTSTUID']+NEW,user_missing=True)
    meta=load_json('data/processed/stu_metadata.json')
    for v in NEW:
        for r in meta['missing_ranges'].get(v,[]):extra.loc[extra[v].between(r['lo'],r['hi']),v]=np.nan
    data=pd.read_parquet(ROOT/'data/processed/pisa2025_stage2c_oecd.parquet').merge(extra,on=['CNT','CNTSTUID'],how='left',validate='one_to_one')
    spec=load_json('results/stage2c_specification.json');rows=[];available=[]
    for i,country in enumerate(spec['candidate_countries'],1):
        g=data.loc[data.CNT.eq(country)];total=g.W_FSTUWT.sum()
        for digital in NEW:
            ok=g[digital].notna();available.append({'country':country,'candidate':digital,'N_valid':int(ok.sum()),'N_total':len(g),
                'coverage_pct':100*g.loc[ok,'W_FSTUWT'].sum()/total,'coverage_75_pass':100*g.loc[ok,'W_FSTUWT'].sum()/total>=75,
                'nationally_absent':not ok.any(),'chosen_M2_core':False,'conceptual_class':'comparison_task_not_IA_specific',
                'selection_uses_AI_coefficients':False,'not_validated_negative_control':True,'official_wording':meta['column_names_to_labels'][digital]})
            mask=m.make_mask(g,m.AI+[digital],m.CORE);sub=g.loc[mask];coverage=100*sub.W_FSTUWT.sum()/total
            for exposure in [digital]+m.AI:
                cats=range(1,7) if exposure=='IC177Q07JA' else range(1,6)
                common={'country':country,'digital_comparator':digital,'exposure':exposure,'base_controls':'CORE','N':len(sub),
                    'weighted_N':sub.W_FSTUWT.sum(),'joint_coverage_pct':coverage,'coverage_75_pass':coverage>=75,
                    'same_students_for_AI_and_digital':True,'not_validated_negative_control':True,'questionnaire_AI_exclusion_explicit':False}
                if not len(sub) or min(sub[exposure].eq(k).sum() for k in cats)<30:
                    rows.append({**common,'domain':'ALL','contrast':'not_estimable','fit_status':'insufficient_support_or_missing',
                        'beta':np.nan,'SE':np.nan,'p_raw':np.nan,'primary_synthesis_eligible':False});continue
                # Explicit flexible indicators; no equal spacing for ordinal time.
                X,terms,_=m.design(sub,[],m.CORE);expos=np.column_stack([sub[exposure].eq(k).to_numpy(float) for k in list(cats)[1:]])
                X=np.column_stack([np.ones(len(sub)),expos,X[:,1:]])
                p=expos.shape[1];terms=['intercept']+[f'{exposure}_{k}' for k in list(cats)[1:]]+terms[1:]
                theta,info=m.fit_arrays(sub,X,terms)
                if theta is None:
                    rows.append({**common,'domain':'ALL','contrast':'not_estimable','fit_status':info['fit_status'],'beta':np.nan,'SE':np.nan,'p_raw':np.nan,'primary_synthesis_eligible':False});continue
                selected=theta[:,:,:,1:1+p];np.savez_compressed(m.SAVE/f'{country}__DIGITAL-MATCHED__CORE__{digital}__{exposure}.npz',theta=selected)
                labels=m.CONTRASTS if exposure!='IC177Q07JA' else ['under_1h_vs_none','1_to_3h_vs_none','over_3_to_5h_vs_none','over_5_to_7h_vs_none','over_7h_vs_none','over_7h_vs_3_to_5h']
                for di,d in enumerate(m.DOM):
                    a=selected[di];ct=np.concatenate([a,(a[:,:,-1]-a[:,:,2])[:,:,None]],axis=2);q,U,B,T=m.combine(ct)
                    for j,label in enumerate(labels):rows.append({**common,'domain':d,'contrast':label,**m.stats(q[j],T[j,j]),
                         'sampling_variance':U[j,j],'between_PV_variance':B[j,j],'fit_status':'estimated','primary_synthesis_eligible':coverage>=75})
        if i%9==0:print(f'Task comparisons {i}/36, {time.time()-start:.1f}s',flush=True)
    m.write(pd.DataFrame(rows),'digital_task_comparison_results.csv');m.write(pd.DataFrame(available),'digital_task_comparison_availability.csv')
    # Required digital deliverable includes all comparators, preserving scopes.
    old=pd.read_csv(ROOT/'results/digital_comparison_controls.csv');old=old.loc[old.model.ne('DIGITAL-TASK-COMPARISON')];old['sample_scope']='own exposure complete cases'
    new=pd.DataFrame(rows);new=new.loc[new.exposure.isin(NEW)].copy();new['model']='DIGITAL-TASK-COMPARISON';new['sample_scope']='same cases as all four AI items'
    m.write(pd.concat([old,new],ignore_index=True),'digital_comparison_controls.csv')
    log('Comparadores de tareas digitales','Navegación, compartir tareas y producción; selección por redacción oficial','No asumir exclusión de IA por ausencia de la palabra IA')
if __name__=='__main__':main()
