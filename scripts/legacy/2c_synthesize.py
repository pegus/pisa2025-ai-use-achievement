from common import ROOT,load_json,save_json,log
import numpy as np,pandas as pd,itertools,json
from functools import lru_cache
from scipy.stats import norm,chi2,spearmanr
from scipy.optimize import linear_sum_assignment
from importlib.util import spec_from_file_location,module_from_spec
sp=spec_from_file_location('models',ROOT/'scripts/2c_models.py');m=module_from_spec(sp);sp.loader.exec_module(m)
sp=spec_from_file_location('syn2b',ROOT/'scripts/2b_synthesize.py');s=module_from_spec(sp);sp.loader.exec_module(s)
AI=m.AI;DOM=m.DOM;CONTRASTS=m.CONTRASTS
def write(df,name):m.write(df,name)
@lru_cache(maxsize=4096)
def arr(country,model,base,exposure):
    if model in ['OLD-M1','OLD-M2']:
        matrices=[np.load(ROOT/f'data/processed/stage2b_model_estimates/{country}_{exposure}_{d}_{"M1" if model=="OLD-M1" else "M2"}.npz')['theta'][:,:,1:5] for d in DOM]
        return np.stack(matrices)
    joint=model=='JOINT-AI-USES'
    f=m.SAVE/f'{country}__{model}__{base}__{"JOINT" if joint else exposure}.npz'
    z=np.load(f);ix=AI.index(exposure) if joint else 0
    return z['theta'][:,:,:,ix,:]
def contrasts(a):return np.concatenate([a,(a[:,:,:,3]-a[:,:,:,2])[:,:,:,None]],axis=3)
def eligible(df,model,base,exposure,domain,contrast):
    return df.loc[df.model.eq(model)&df.base_controls.eq(base)&df.exposure.eq(exposure)&df.domain.eq(domain)&df.contrast.eq(contrast)&df.primary_synthesis_eligible&df.fit_status.eq('estimated')]
def paired_change(df,exposure,domain,contrast,newmodel,newbase,oldmodel,oldbase,countries):
    di=DOM.index(domain);j=CONTRASTS.index(contrast);qs=[];ts=[]
    for c in countries:
        a=contrasts(arr(c,newmodel,newbase,exposure))[di,:,:,j];b=contrasts(arr(c,oldmodel,oldbase,exposure))[di,:,:,j]
        q,U,B,T=m.combine((a-b)[:,:,None]);qs.append(q[0]);ts.append(T[0,0])
    if not qs:return {'K':0,'delta_beta':np.nan,'SE_delta':np.nan}
    beta=float(np.mean(qs));v=sum(ts)/len(qs)**2;r=m.stats(beta,v)
    return {'K':len(qs),'delta_beta':beta,'SE_delta':r['SE'],'CI95_low_delta':r['CI95_low'],'CI95_high_delta':r['CI95_high'],'p_delta':r['p_raw'],
      'CI90_low_delta':beta-1.6448536269514722*r['SE'],'CI90_high_delta':beta+1.6448536269514722*r['SE'],
      'equivalence_5_points_pass':abs(beta)+1.6448536269514722*r['SE']<5,'countries':';'.join(countries)}
def main():
    df=pd.read_csv(ROOT/'results/stage2c_all_national_models.csv');spec=load_json('results/stage2c_specification.json');full21=set(spec['full21'])
    old1=pd.read_csv(ROOT/'results/country_effects_M1.csv');old1['model']='OLD-M1';old1['base_controls']='NONE';old1['primary_synthesis_eligible']=old1.primary_synthesis_eligible.astype(bool)
    old2=pd.read_csv(ROOT/'results/country_effects_M2.csv');old2['model']='OLD-M2';old2['base_controls']='FULL'
    augmented=pd.concat([df,old1,old2],ignore_index=True)
    summary=[];reml=[]
    main_models=['M2-CORE','M2-FULL','M2-SCHOOL-FE','M3-CONFOUNDERS','M3-INCLUDING-POTENTIAL-MEDIATORS','JOINT-AI-USES','M2-CORE-PRIMARY-REPETITION','DIGITAL-COMPARISON']
    for (model,base,exp,domain,contrast),g in df.loc[df.model.isin(main_models)].groupby(['model','base_controls','exposure','domain','contrast']):
        g=g.loc[g.primary_synthesis_eligible&g.fit_status.eq('estimated')]
        summary.append({'model':model,'base_controls':base,'exposure':exp,'domain':domain,'contrast':contrast,**s.summarize(g)})
        reml.append({'model':model,'base_controls':base,'exposure':exp,'domain':domain,'contrast':contrast,**s.reml(g)})
    summary=pd.DataFrame(summary);summary['q_FDR']=summary.groupby(['model','base_controls']).p_raw.transform(s.bh)
    summary['FDR_family']='all exposure/domain/frequency tests within model and base; secondary stage2c'
    write(summary,'stage2c_equal_weight_summary.csv');write(pd.DataFrame(reml),'stage2c_REML_summary.csv')
    # Country/support changes are shown separately from same-student controls.
    progression=[]
    for exp,domain,contrast in itertools.product(AI,DOM,CONTRASTS):
        a=eligible(augmented,'OLD-M1','NONE',exp,domain,contrast)
        b=a.loc[a.country.isin(full21)]
        c=eligible(augmented,'M2-CORE','CORE',exp,domain,contrast)
        d=c.loc[c.country.isin(full21)]
        e=eligible(augmented,'M2-FULL','FULL',exp,domain,contrast)
        groups={'A_M1_36':a,'B_M1_21':b,'C_M2_CORE_all_eligible':c,'D_M2_CORE_21':d,'E_M2_FULL_21':e}
        row={'exposure':exp,'domain':domain,'contrast':contrast}
        for label,gg in groups.items():
            info=s.summarize(gg)
            for field in ['beta','SE','K','N','countries','CI95_low','CI95_high']:row[label+'_'+field]=info.get(field,np.nan)
        row['delta_country_selection_B_minus_A']=b.beta.mean()-a.beta.mean()
        row['delta_CORE_country_selection_D_minus_C']=d.beta.mean()-c.beta.mean()
        cset=set(c.country);old_on_c=a.loc[a.country.isin(cset)]
        core_sample=eligible(augmented,'M1-CORE-SAMPLE','CORE',exp,domain,contrast);core_sample=core_sample.loc[core_sample.country.isin(cset)]
        row['A_to_C_country_component']=old_on_c.beta.mean()-a.beta.mean()
        row['A_to_C_student_selection_component']=core_sample.beta.mean()-old_on_c.beta.mean()
        row['A_to_C_controls_same_students_component']=c.beta.mean()-core_sample.beta.mean()
        row['A_to_C_total']=c.beta.mean()-a.beta.mean()
        assert abs(sum(row[k] for k in ['A_to_C_country_component','A_to_C_student_selection_component','A_to_C_controls_same_students_component'])-row['A_to_C_total'])<1e-8
        for title,new,old,base,newg,oldg in [
             ('CORE_adjustment_same_students','M2-CORE','M1-CORE-SAMPLE','CORE',c,core_sample),
             ('FULL_adjustment_same_students','M2-FULL','M1-FULL-SAMPLE','FULL',e,eligible(augmented,'M1-FULL-SAMPLE','FULL',exp,domain,contrast)),
             ('CORE_to_FULL_student_selection','M2-CORE-FULL-SAMPLE','M2-CORE','CORE',eligible(augmented,'M2-CORE-FULL-SAMPLE','CORE',exp,domain,contrast),d),
             ('CORE_to_FULL_extra_controls_same_students','M2-FULL','M2-CORE-FULL-SAMPLE','FULL',e,eligible(augmented,'M2-CORE-FULL-SAMPLE','CORE',exp,domain,contrast))]:
            countries=sorted(set(newg.country)&set(oldg.country)&(full21 if title!='CORE_adjustment_same_students' else cset))
            oldbase='CORE' if title=='CORE_to_FULL_extra_controls_same_students' else base
            info=paired_change(augmented,exp,domain,contrast,new,base,old,oldbase,countries)
            for k,v in info.items():row[title+'_'+k]=v
        fset=set(e.country);fullsample=eligible(augmented,'M1-FULL-SAMPLE','FULL',exp,domain,contrast);fullsample=fullsample.loc[fullsample.country.isin(fset)]
        row['B_to_E_student_selection_component']=fullsample.beta.mean()-b.beta.mean()
        row['B_to_E_controls_same_students_component']=e.beta.mean()-fullsample.beta.mean()
        row['D_to_E_total']=e.beta.mean()-d.beta.mean()
        row['note']='algebraic decomposition of descriptive adjusted associations; same students/weights for controls; not causal'
        progression.append(row)
    write(pd.DataFrame(progression),'model_progression_same_sample.csv')
    changes=[]
    comparisons=[('M2-SCHOOL-FE','M2-NO-FE-SAME-SAMPLE'),
        ('M3-CONFOUNDERS','M2-SAME-SAMPLE-M3-CONFOUNDERS'),
        ('M3-INCLUDING-POTENTIAL-MEDIATORS','M2-SAME-SAMPLE-M3-INCLUDING-POTENTIAL-MEDIATORS'),
        ('JOINT-AI-USES','SEPARATE-AI-JOINT-SAMPLE'),
        ('M2-CORE-PRIMARY-REPETITION','M2-CORE-REPETITION-SAMPLE')]
    for newmodel,oldmodel in comparisons:
        for base in ['CORE','FULL']:
            if base=='FULL' and newmodel=='M2-CORE-PRIMARY-REPETITION':continue
            for exp,domain,contrast in itertools.product(AI,DOM,CONTRASTS):
                newg=eligible(augmented,newmodel,base,exp,domain,contrast);oldg=eligible(augmented,oldmodel,base,exp,domain,contrast)
                countries=sorted(set(newg.country)&set(oldg.country));newg=newg.loc[newg.country.isin(countries)];oldg=oldg.loc[oldg.country.isin(countries)]
                changes.append({'new_model':newmodel,'comparison_model':oldmodel,'base_controls':base,'exposure':exp,'domain':domain,'contrast':contrast,
                   'new_beta':newg.beta.mean(),'old_beta_same_sample':oldg.beta.mean(),
                   'percent_attenuation_magnitude':100*(1-abs(newg.beta.mean())/abs(oldg.beta.mean())) if len(oldg) and abs(oldg.beta.mean())>1e-8 else np.nan,
                   **paired_change(augmented,exp,domain,contrast,newmodel,base,oldmodel,base,countries)})
    write(pd.DataFrame(changes),'stage2c_paired_model_changes.csv')
    # Complete covariance between domain coefficients, same national sample.
    specificity=[];national_specificity=[];ec=pd.read_csv(ROOT/'results/stage2c_country_characteristics.csv')
    for (model,base) in summary.loc[summary.model.ne('DIGITAL-COMPARISON'),['model','base_controls']].drop_duplicates().itertuples(index=False,name=None):
        for exp,contrast,other in itertools.product(AI,['daily_vs_never','daily_vs_weekly'],['MATH','SCIE']):
            sets=[set(eligible(augmented,model,base,exp,d,contrast).country) for d in ['READ',other]];countries=sorted(sets[0]&sets[1]);K=len(countries)
            estimates=[];Ulist=[];Blist=[];Tlist=[];bounds=[];std_deltas=[]
            for country in countries:
                values=contrasts(arr(country,model,base,exp));j=CONTRASTS.index(contrast)
                a=values[0,:,:,j];b=values[DOM.index(other),:,:,j]
                q,U,B,T=m.combine((a-b)[:,:,None]);estimates.append(q[0]);Ulist.append(U[0,0]);Blist.append(B[0,0]);Tlist.append(T[0,0])
                _,ua,ba,ta=m.combine(a[:,:,None]);_,ub,bb,tb=m.combine(b[:,:,None])
                ra=a[:,1:]-a[:,[0]];rb=b[:,1:]-b[:,[0]]
                covs=ra@rb.T/20;ii,jj=linear_sum_assignment(covs)
                sampling_upper=ua[0,0]+ub[0,0]-2*np.mean(covs[ii,jj])
                b_upper=(np.sqrt(ba[0,0])+np.sqrt(bb[0,0]))**2;bound=sampling_upper+1.1*b_upper;bounds.append(bound)
                national_specificity.append({'country':country,'model':model,'base_controls':base,'exposure':exp,'contrast':contrast,'difference':'READ_minus_'+other,
                    'beta_difference':q[0],'sampling_variance_paired':U[0,0],'between_PV_variance_paired':B[0,0],'sampling_covariance_paired':(ua[0,0]+ub[0,0]-U[0,0])/2,
                    'total_covariance_paired':(ta[0,0]+tb[0,0]-T[0,0])/2,'paired_total_variance':T[0,0],
                    'sampling_variance_upper_any_PV_pairing':sampling_upper,'between_PV_variance_upper':b_upper,'conservative_total_variance':bound})
                rr=ec.loc[ec.country.eq(country)&ec.exposure.eq(exp)].iloc[0]
                std_deltas.append(a[:,0].mean()/rr.national_SD_READ-b[:,0].mean()/rr['national_SD_'+other])
            if K:
                beta=float(np.mean(estimates));conservative=sum(bounds)/K**2;paired=sum(Tlist)/K**2
                specificity.append({'model':model,'base_controls':base,'exposure':exp,'contrast':contrast,'difference':'READ_minus_'+other,'K':K,
                    'countries':';'.join(countries),**m.stats(beta,conservative),'SE_paired_PV':np.sqrt(paired),
                    'p_paired_PV':2*norm.sf(abs(beta)/np.sqrt(paired)),
                    'paired_CI95_low':beta-1.95996398454*np.sqrt(paired),'paired_CI95_high':beta+1.95996398454*np.sqrt(paired),
                    'sampling_variance_paired_sum_K2':sum(Ulist)/K**2,'between_PV_variance_paired_sum_K2':sum(Blist)/K**2,
                    'variance_conservative_bound':conservative,'mean_standardized_difference_SD':np.mean(std_deltas),
                    'primary_variance_method':'max sampling variance across PV pairings plus Cauchy bound for B; paired covariance sensitivity',
                    'joint_PV_alignment_2025_documented':False})
            else:specificity.append({'model':model,'base_controls':base,'exposure':exp,'contrast':contrast,'difference':'READ_minus_'+other,'K':0,'beta':np.nan,'p_raw':np.nan})
    specificity=pd.DataFrame(specificity);specificity['q_FDR_16']=specificity.groupby(['model','base_controls']).p_raw.transform(s.bh)
    specificity['q_FDR_16_paired_PV']=specificity.groupby(['model','base_controls']).p_paired_PV.transform(s.bh)
    write(specificity,'domain_specificity_tests.csv');write(pd.DataFrame(national_specificity),'domain_specificity_national_covariance.csv')
    # Learn-vs-other within-domain pattern tests with correlated fits.
    patterns=[]
    for (model,base) in summary.loc[summary.model.ne('DIGITAL-COMPARISON'),['model','base_controls']].drop_duplicates().itertuples(index=False,name=None):
        for other,domain in itertools.product(AI[:3],DOM):
            sets=[set(eligible(augmented,model,base,v,domain,'daily_vs_never').country) for v in [other,AI[3]]];countries=sorted(sets[0]&sets[1]);K=len(countries)
            qs=[];ts=[]
            for country in countries:
                di=DOM.index(domain);a=arr(country,model,base,AI[3])[di];b=arr(country,model,base,other)[di]
                q,U,B,T=m.combine(a-b);qs.append(q);ts.append(T)
            if K:
                q=np.mean(qs,axis=0);T=np.sum(ts,axis=0)/K**2;wald=float(q@np.linalg.solve(T,q))
                row={'model':model,'base_controls':base,'other_exposure':other,'domain':domain,'K':K,'Wald_chi2':wald,'df':4,'p_raw':chi2.sf(wald,4),'countries':';'.join(countries)}
                for j,label in enumerate(CONTRASTS[:4]):row[label+'_learn_minus_other']=q[j];row[label+'_SE']=np.sqrt(T[j,j])
                patterns.append(row)
    patterns=pd.DataFrame(patterns);patterns['q_FDR_9']=patterns.groupby(['model','base_controls']).p_raw.transform(s.bh);write(patterns,'stage2c_learn_pattern_tests.csv')
    # Reverse-causality prevalence: independent-country equal averages.
    reverse=pd.read_csv(ROOT/'results/reverse_causality_diagnostics.csv');rs=[]
    for (exp,history,group),g in reverse.groupby(['exposure','diagnostic','group']):
        g=g.loc[g.joint_coverage_pct.ge(75)&g.estimate.notna()&g.SE.notna()];K=len(g)
        if K:
            beta=g.estimate.mean();v=(g.SE**2).sum()/K**2
            rs.append({'exposure':exp,'diagnostic':history,'group':group,'K':K,'estimate':beta,'SE':np.sqrt(v),'CI95_low':beta-1.959964*np.sqrt(v),'CI95_high':beta+1.959964*np.sqrt(v),
              'p_raw':2*norm.sf(abs(beta)/np.sqrt(v)) if v>0 else np.nan,'countries':';'.join(sorted(g.country)),'temporal_status':g.temporal_status.iloc[0]})
    rs=pd.DataFrame(rs);rs['q_FDR_diagnostic']=np.nan
    ix=rs.group.eq('daily_minus_never');rs.loc[ix,'q_FDR_diagnostic']=s.bh(rs.loc[ix,'p_raw']);write(rs,'reverse_causality_summary.csv')
    # Joint precision/sign changes on same cases, never interpreted as causal.
    joint=pd.read_csv(ROOT/'results/joint_AI_uses_model.csv');joint=joint.drop(columns=[c for c in joint if c.endswith('_separate_same_sample') or c in ['SE_ratio_joint_to_separate','sign_change_from_separate','precision_inflation_gt_2']],errors='ignore');sep=df.loc[df.model.eq('SEPARATE-AI-JOINT-SAMPLE')]
    j=joint.merge(sep[['country','base_controls','exposure','domain','contrast','beta','SE']],on=['country','base_controls','exposure','domain','contrast'],suffixes=('','_separate_same_sample'),validate='one_to_one')
    j['SE_ratio_joint_to_separate']=j.SE/j.SE_separate_same_sample;j['sign_change_from_separate']=np.sign(j.beta)!=np.sign(j.beta_separate_same_sample)
    j['precision_inflation_gt_2']=j.SE_ratio_joint_to_separate>2;write(j,'joint_AI_uses_model.csv')
    # Associations of country coefficients with national features are ecological.
    eco=pd.read_csv(ROOT/'results/stage2c_country_characteristics.csv');erows=[]
    for (model,base,exp,domain,contrast),g in df.loc[df.model.isin(main_models)&df.exposure.isin(AI)&df.contrast.isin(['daily_vs_never','daily_vs_weekly'])&df.primary_synthesis_eligible].groupby(['model','base_controls','exposure','domain','contrast']):
        z=g.merge(eco,on=['country','exposure'])
        for feature in ['AI_any_pct','AI_daily_pct','ESCS_mean','coverage_pct','national_mean_'+domain]:
            valid=z[['beta',feature]].dropna();K=len(valid)
            if K>=4 and valid[feature].nunique()>1:r,p=spearmanr(valid.beta,valid[feature])
            else:r=p=np.nan
            erows.append({'model':model,'base_controls':base,'exposure':exp,'domain':domain,'contrast':contrast,'country_characteristic':feature,
                'K':K,'Spearman_rho':r,'p_exploratory':p,'causal':False,'ecological_only':True})
    write(pd.DataFrame(erows),'heterogeneity_country_correlates.csv')
    print('Summary counts\n',summary.groupby(['model','base_controls']).K.agg(['min','max']).to_string(),flush=True)
    print('READ daily never\n',summary.loc[summary.domain.eq('READ')&summary.contrast.eq('daily_vs_never'),['model','base_controls','exposure','beta','SE','K','q_FDR']].to_string(index=False),flush=True)
    log('Síntesis 2C','Descomposición exacta, cambios emparejados, diferencias de dominios y patrones','Varianzas nacionales independientes, inferencia secundaria y covarianza BRR')
if __name__=='__main__':main()
