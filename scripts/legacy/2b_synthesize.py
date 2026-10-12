from common import ROOT,load_json,save_json,log
from importlib.util import spec_from_file_location,module_from_spec
import numpy as np
import pandas as pd
from scipy.stats import norm,chi2,t
from scipy.optimize import minimize_scalar

spec=spec_from_file_location('national',ROOT/'scripts/2b_national_models.py');national=module_from_spec(spec);spec.loader.exec_module(national)
AI=national.AI;DOM=national.DOM;CONTRASTS=national.CONTRASTS
def write(df,name):df.to_csv(ROOT/'results'/name,index=False,encoding='utf-8-sig',float_format='%.12g')
def bh(values):
    values=np.asarray(values,dtype=float);q=np.full(len(values),np.nan);ok=np.flatnonzero(np.isfinite(values))
    order=ok[np.argsort(values[ok])];n=len(order)
    if n:q[order]=np.minimum(1,np.minimum.accumulate((values[order]*n/np.arange(1,n+1))[::-1])[::-1])
    return q
def summarize(g):
    K=len(g)
    if not K:return {'K':0,'beta':np.nan,'SE':np.nan,'CI95_low':np.nan,'CI95_high':np.nan,'p_raw':np.nan,'N':0,'weighted_N':0,
        'countries':'','coverage':np.nan,'beta_min':np.nan,'beta_max':np.nan,'proportion_beta_lt_0':np.nan,'proportion_beta_gt_0':np.nan,
        'between_country_beta_SD':np.nan,'Cochran_Q':np.nan,'Q_p':np.nan,'I2_pct':np.nan,'variance':np.nan,'status':'no_eligible_countries'}
    b=g.beta.to_numpy();v=g.SE.to_numpy()**2;mu=float(b.mean());var=float(v.sum()/K**2)
    r=national.stats(mu,var);r.update({'beta_OECD_equal':mu,'K':K,'N':int(g.N.sum()),'weighted_N':g.weighted_N.sum(),
        'countries':';'.join(sorted(g.country)),'coverage':g.joint_coverage_pct.mean(),'coverage_min':g.joint_coverage_pct.min(),
        'coverage_max':g.joint_coverage_pct.max(),'beta_min':b.min(),'beta_max':b.max(),
        'proportion_beta_lt_0':float((b<0).mean()),'proportion_beta_gt_0':float((b>0).mean()),
        'between_country_beta_SD':float(b.std(ddof=1)) if K>1 else np.nan,'variance':var,'status':'estimated',
        'sampling_variance_sum_over_K2':g.sampling_variance.sum()/K**2,'between_PV_contribution_sum_over_K2':1.1*g.between_PV_variance.sum()/K**2})
    if K>1:
        iv=1/v;ivmu=np.dot(iv,b)/iv.sum();Q=float(np.dot(iv,(b-ivmu)**2));r.update({'Cochran_Q':Q,'Q_df':K-1,'Q_p':chi2.sf(Q,K-1),
            'I2_pct':max(0,100*(Q-K+1)/Q) if Q>0 else 0})
    else:r.update({'Cochran_Q':np.nan,'Q_df':0,'Q_p':np.nan,'I2_pct':np.nan})
    return r
def reml(g):
    if len(g)<2:return {'K':len(g),'status':'not_estimable_K_lt_2'}
    b=g.beta.to_numpy();v=g.SE.to_numpy()**2
    def objective(tau):
        w=1/(v+tau);mu=np.dot(w,b)/w.sum()
        return .5*(np.log(v+tau).sum()+np.log(w.sum())+np.dot(w,(b-mu)**2))
    opt=minimize_scalar(objective,bounds=(0,max(1,10*b.var(ddof=1)+10*v.mean())),method='bounded')
    tau=0. if objective(0)<=opt.fun else float(opt.x);w=1/(v+tau);mu=np.dot(w,b)/w.sum()
    scale=max(1.,float(np.dot(w,(b-mu)**2)/(len(g)-1)));se=np.sqrt(scale/w.sum());critical=t.ppf(.975,len(g)-1)
    return {'K':len(g),'beta_REML':mu,'tau2_REML':tau,'SE_modified_HK':se,'CI95_low':mu-critical*se,'CI95_high':mu+critical*se,
            'p_raw':2*t.sf(abs(mu/se),len(g)-1),'status':'secondary_REML_modified_Hartung_Knapp','countries':';'.join(sorted(g.country))}
def main():
    assert load_json('results/fay2025_validation_status.json')['status']=='PASS'
    tables={m:pd.read_csv(ROOT/f'results/country_effects_{m}.csv') for m in ['M1','M2']}
    uh=pd.read_csv(ROOT/'results/une_heure_oecd.csv').set_index('country');scenarios=[('A_75',75,None),('B_80',80,None),('C_85',85,None),('D_90',90,None),('E_UH_le_5',75,'le5'),('F_no_UH_observed',75,'zero'),('G_all_75',75,None)]
    summaries={};sens=[];metas=[]
    for model,df in tables.items():
        estimated=df.loc[df.fit_status.eq('estimated')&df.country_item_eligible].copy()
        base=[]
        for exposure in AI:
            for domain in DOM:
                for contrast in CONTRASTS:
                    g=estimated.loc[estimated.exposure.eq(exposure)&estimated.domain.eq(domain)&estimated.contrast.eq(contrast)&estimated.joint_coverage_pct.ge(75)]
                    s={'model':model,'exposure':exposure,'domain':domain,'contrast':contrast,**summarize(g)};base.append(s)
                    if model=='M2':metas.append({'exposure':exposure,'domain':domain,'contrast':contrast,**reml(g)})
        summary=pd.DataFrame(base);assert len(summary)==60
        summary['q_FDR']=bh(summary.p_raw);summary['FDR_family']='60 M2 primary contrasts' if model=='M2' else '60 M1 descriptive contrasts; secondary'
        write(summary,f'oecd_equal_weight_summary_{model}.csv');summaries[model]=summary
        if model=='M2':write(summary,'primary_contrasts_M2.csv')
        for label,threshold,filterUH in scenarios:
            scenario=[]
            for exposure in AI:
                for domain in DOM:
                    for contrast in CONTRASTS:
                        g=estimated.loc[estimated.exposure.eq(exposure)&estimated.domain.eq(domain)&estimated.contrast.eq(contrast)&estimated.joint_coverage_pct.ge(threshold)]
                        if filterUH=='le5':g=g.loc[g.country.map(uh.weighted_pct_UH).le(5)]
                        if filterUH=='zero':g=g.loc[g.country.map(uh.N_UH).eq(0)]
                        baseline=summary.loc[summary.exposure.eq(exposure)&summary.domain.eq(domain)&summary.contrast.eq(contrast)].iloc[0]
                        row={'model':model,'scenario':label,'joint_coverage_threshold_pct':threshold,'UH_filter':filterUH or 'none','exposure':exposure,'domain':domain,'contrast':contrast,
                             **summarize(g),'baseline_beta':baseline.beta,'baseline_K':baseline.K}
                        row['beta_change_from_A']=row['beta']-baseline.beta
                        row['same_sign_as_A']=bool(np.sign(row['beta'])==np.sign(baseline.beta)) if np.isfinite(row['beta']) and np.isfinite(baseline.beta) else None
                        scenario.append(row)
            scenario=pd.DataFrame(scenario);scenario['q_FDR']=bh(scenario.p_raw);scenario['FDR_family']='60 contrasts within scenario; secondary sensitivity'
            sens.extend(scenario.to_dict('records'))
    sens=pd.DataFrame(sens);write(sens,'selection_sensitivity.csv');write(pd.DataFrame(metas),'secondary_REML_M2.csv')
    # Correlated contrasts between exposure-specific fits, with common country
    # set, same national BRR/PV labels; countries themselves remain independent.
    h4=[];h4levels=[];h4sens=[];df=tables['M2'];path=ROOT/'data/processed/stage2b_model_estimates'
    eligible=df.loc[df.fit_status.eq('estimated')&df.primary_synthesis_eligible]
    for other in AI[:3]:
        for domain in DOM:
            sets=[set(eligible.loc[eligible.exposure.eq(v)&eligible.domain.eq(domain),'country']) for v in [AI[3],other]]
            countries=sorted(sets[0]&sets[1]);qs=[];ts=[];national_patterns={}
            for c in countries:
                learn=np.load(path/f'{c}_{AI[3]}_{domain}_M2.npz')['theta'][:,:,1:5]
                compare=np.load(path/f'{c}_{other}_{domain}_M2.npz')['theta'][:,:,1:5]
                q,U,B,T=national.combine(learn-compare);qs.append(q);ts.append(T);national_patterns[c]=(q,T)
            K=len(countries)
            if K:
                q=np.mean(qs,axis=0);T=np.sum(ts,axis=0)/K**2;wald=float(q@np.linalg.solve(T,q))
                h4.append({'learn_exposure':AI[3],'other_exposure':other,'domain':domain,'K':K,'countries':';'.join(countries),'Wald_chi2':wald,'df':4,'p_raw':chi2.sf(wald,4),
                           'interpretation':'difference of association patterns among exposure-specific respondents; not causal'})
                for j,label in enumerate(CONTRASTS[:4]):h4levels.append({'other_exposure':other,'domain':domain,'contrast':label,'K':K,**national.stats(q[j],T[j,j])})
            else:h4.append({'learn_exposure':AI[3],'other_exposure':other,'domain':domain,'K':0,'countries':'','Wald_chi2':np.nan,'df':4,'p_raw':np.nan})
            for label,threshold,filterUH in scenarios:
                selected=[]
                for c in countries:
                    link=eligible.loc[eligible.country.eq(c)&eligible.domain.eq(domain)&eligible.exposure.isin([AI[3],other]),'joint_coverage_pct'].min()
                    if link<threshold:continue
                    if filterUH=='le5' and uh.loc[c,'weighted_pct_UH']>5:continue
                    if filterUH=='zero' and uh.loc[c,'N_UH']!=0:continue
                    selected.append(c)
                if selected:
                    q=np.mean([national_patterns[c][0] for c in selected],axis=0);T=np.sum([national_patterns[c][1] for c in selected],axis=0)/len(selected)**2
                    wald=float(q@np.linalg.solve(T,q));prob=chi2.sf(wald,4)
                else:wald=prob=np.nan
                h4sens.append({'scenario':label,'other_exposure':other,'domain':domain,'K':len(selected),'countries':';'.join(selected),
                               'Wald_chi2':wald,'df':4,'p_raw':prob})
    h4=pd.DataFrame(h4);h4['q_FDR_secondary_9']=bh(h4.p_raw);write(h4,'learn_vs_other_pattern_tests_M2.csv')
    write(pd.DataFrame(h4levels),'learn_vs_other_level_differences_M2.csv')
    h4sens=pd.DataFrame(h4sens);h4sens['q_FDR_secondary_9']=h4sens.groupby('scenario').p_raw.transform(lambda x:bh(x))
    write(h4sens,'learn_vs_other_pattern_sensitivity_M2.csv')
    # Difference in M1/M2 on exactly the M2 country list to separate changes in
    # national inclusion from conditional associations (student samples differ).
    comparisons=[]
    for r in summaries['M2'].to_dict('records'):
        countries=set(str(r['countries']).split(';'));d=tables['M1']
        g=d.loc[d.country.isin(countries)&d.exposure.eq(r['exposure'])&d.domain.eq(r['domain'])&d.contrast.eq(r['contrast'])&d.fit_status.eq('estimated')]
        comparisons.append({'exposure':r['exposure'],'domain':r['domain'],'contrast':r['contrast'],'K_M2':r['K'],'M2_beta':r['beta'],
                            'M1_beta_same_countries':g.beta.mean(),'M1_beta_all_eligible':summaries['M1'].loc[summaries['M1'].exposure.eq(r['exposure'])&summaries['M1'].domain.eq(r['domain'])&summaries['M1'].contrast.eq(r['contrast']),'beta'].iloc[0],
                            'note':'country list held fixed; respondent samples differ; not a causal decomposition'})
    write(pd.DataFrame(comparisons),'M1_M2_country_set_comparison.csv')
    log('Síntesis igualitaria y sensibilidades M2','60 contrastes principales, siete escenarios y nueve pruebas secundarias de patrones',
        'Combinar varianzas nacionales independientes; no incluir ISR/USA; no ajustar M3/M4/M5')
    print('M2 country counts\n',summaries['M2'].groupby(['exposure','domain']).K.first().to_string(),flush=True)
    print('READ primary\n',summaries['M2'].loc[summaries['M2'].domain.eq('READ'),['exposure','contrast','beta','SE','q_FDR','K','proportion_beta_lt_0']].to_string(index=False),flush=True)

if __name__=='__main__':main()
