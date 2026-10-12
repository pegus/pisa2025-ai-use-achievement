"""Descriptive selection audit only: no regression and no unverified Fay factor."""
from common import ROOT,load_json,save_json,log
import numpy as np
import pandas as pd

AI=[f'ST438Q0{i}DA' for i in range(1,5)]
VARS=AI+['AIUSESCH','ST436Q16DA']
DOMAINS=['READ','MATH','SCIE']
def write(df,name):df.to_csv(ROOT/'results'/name,index=False,encoding='utf-8-sig',float_format='%.10g')
def count(mask,w):return int(mask.sum()),float(w[mask].sum())

def main():
    raw=pd.read_parquet(ROOT/'data/processed/selection_audit_raw.parquet')
    meta=load_json('data/processed/stu_metadata.json')
    names=load_json('data/documentation/codebook_parsed.json')['STU']['CNT']['values']
    assert len(raw)==755721 and raw.W_FSTUWT.gt(0).all()
    for d in DOMAINS:
        for m in range(1,11):
            # No arbitrary bounds: apply only documented SPSS missing ranges.
            v=f'PV{m}{d}'
            for r in meta['missing_ranges'].get(v,[]):
                raw.loc[raw[v].between(r['lo'],r['hi']),v]=np.nan
    structural=raw[AI].eq(97)
    raw['ST438_status']=np.select([structural.all(axis=1),structural.any(axis=1),raw[AI].isin([1,2,3,4,5,98,99]).any(axis=1)],
                                ['not_administered','mixed_structural','administered_evidence'],default='unknown')
    # Identification uses official form labels, observed mode and national option,
    # plus independent questionnaire-content/missing-code checks below.
    uh=raw.BOOKID.eq(199)&raw.ADMINMODE.eq(1)&structural.all(axis=1)&raw.ST436Q16DA.eq(7)
    assert not (raw.BOOKID.eq(199)&~uh).any()
    raw['audit_mode']=np.select([uh,raw.ADMINMODE.eq(2)&raw.BOOKID.between(16,27),raw.ADMINMODE.eq(1)&raw.BOOKID.between(1,12),
          raw.ADMINMODE.eq(1)&raw.BOOKID.between(13,15),raw.ADMINMODE.eq(1)&raw.BOOKID.between(201,209)],
          ['UH','PBA','CBA_standard','CBA_FLA','CBA_UO_labelled'],default='unresolved_form')
    # Do not assign unknown forms or mixed structural patterns to eligible group.
    raw['ST438_eligible_proxy']=raw.ADMINMODE.eq(1)&~uh&raw.audit_mode.ne('unresolved_form')&raw.ST438_status.eq('administered_evidence')
    raw['ST438_four_valid']=raw[AI].isin([1,2,3,4,5]).all(axis=1)
    raw[['CNT','CNTSTUID','ADMINMODE','BOOKID','Option_UH','audit_mode','ST438_status','ST438_eligible_proxy','ST438_four_valid']].to_parquet(
        ROOT/'data/processed/selection_audit_classification.parquet',index=False,compression='zstd')
    coverage=[]; modes=[];senate=[];patterns=[];uhrows=[];perf=[];perpv=[];contrasts=[];eligibility=[]
    for c,g in raw.groupby('CNT',sort=True):
        w=g.W_FSTUWT.to_numpy();total=float(w.sum());n=len(g);oecd=int(g.OECD.iloc[0])
        base={'country':c,'country_name':names.get(c,c),'OECD':oecd,'N_total':n,'weighted_N_total':total}
        modecols={}
        for key,mask in [('CBA',g.ADMINMODE.eq(1).to_numpy()),('PBA',g.ADMINMODE.eq(2).to_numpy()),
                         ('ADMINMODE_other',(~g.ADMINMODE.isin([1,2])&g.ADMINMODE.notna()).to_numpy()),('ADMINMODE_missing',g.ADMINMODE.isna().to_numpy())]:
            nn,ww=count(mask,w);modecols.update({f'N_{key}':nn,f'weighted_N_{key}':ww,f'weighted_pct_{key}':100*ww/total})
        for typ,field in [('ADMINMODE','ADMINMODE'),('validated_form','audit_mode')]:
            for value in ([1.,2.,'other','missing'] if field=='ADMINMODE' else ['CBA_standard','CBA_FLA','CBA_UO_labelled','UH','PBA','unresolved_form']):
                mask=(g[field].isna() if value=='missing' else (~g[field].isin([1,2])&g[field].notna()) if value=='other' else g[field].eq(value)).to_numpy()
                nn,ww=count(mask,w);modes.append({**base,'classification':typ,'mode':value,'N':nn,'weighted_N':ww,'weighted_pct':100*ww/total})
        for v in VARS:
            x=g[v].to_numpy();critical=v=='ST436Q16DA';codes=[5,6,7,8,9] if critical else [95,96,97,98,99]
            valid=np.isin(x,[1,2,3,4] if critical else [1,2,3,4,5]) if v!='AIUSESCH' else np.isfinite(x)&~np.isin(x,codes)
            cats={'valid':valid,'valid_skip':x==codes[0],'system_missing_code':x==codes[1],
                  'structural_not_administered':x==codes[2],'invalid_response':x==codes[3],'no_response':x==codes[4],'system_null':pd.isna(x)}
            assigned=np.vstack(list(cats.values())).sum(axis=0)
            assert (assigned<=1).all()
            cats['unexpected_code']=assigned==0
            row={**base,**modecols,'variable':v,'structural_code':codes[2],'denominator':'all PUF respondents in country; W_FSTUWT',
                 'coverage_threshold_pct':75.,'coverage_75_pass':100*w[valid].sum()/total>=75.,
                 'operational_flag':'valid item/index response; not national adjudication certification'}
            for k,mask in cats.items():
                nn,ww=count(mask,w);row.update({f'N_{k}':nn,f'weighted_N_{k}':ww,f'weighted_pct_{k}':100*ww/total})
            assert sum(row[f'N_{k}'] for k in cats)==n
            assert np.isclose(sum(row[f'weighted_N_{k}'] for k in cats),total)
            denom_admin=total-row['weighted_N_structural_not_administered']
            row['valid_pct_among_nonstructural']=100*row['weighted_N_valid']/denom_admin if denom_admin>0 else np.nan
            row['nonstructural_75_pass']=100*denom_admin/total>=75
            coverage.append(row)
        expected=5000*w/total;observed=g.SENWT.to_numpy();err=np.abs(observed-expected)
        senate.append({**base,'SENWT_sum':float(observed.sum()),'normalization_constant':5000/total,
                       'max_absolute_difference':float(err.max()),'max_relative_difference':float((err/expected).max()),
                       'allclose':bool(np.allclose(observed,expected,rtol=1e-7,atol=1e-7)),
                       'sum_5000_pass':bool(np.isclose(observed.sum(),5000,rtol=1e-7,atol=.001))})
        for (mode,status),s in g.groupby(['audit_mode','ST438_status']):
            patterns.append({**base,'audit_mode':mode,'ST438_status':status,'N':len(s),'weighted_N':s.W_FSTUWT.sum(),'weighted_pct':100*s.W_FSTUWT.sum()/total})
        masks={'ALL':np.ones(n,dtype=bool),'ST438_administered':g.ST438_status.eq('administered_evidence').to_numpy(),
               'ST438_not_administered':g.ST438_status.eq('not_administered').to_numpy(),
               'ST438_mixed_structural':g.ST438_status.eq('mixed_structural').to_numpy(),'ST438_unknown':g.ST438_status.eq('unknown').to_numpy(),
               'CBA':g.ADMINMODE.eq(1).to_numpy(),'PBA':g.ADMINMODE.eq(2).to_numpy(),'UH':g.audit_mode.eq('UH').to_numpy(),
               'CBA_standard':g.audit_mode.eq('CBA_standard').to_numpy(),'CBA_UO_labelled':g.audit_mode.eq('CBA_UO_labelled').to_numpy(),
               'unresolved_form':g.audit_mode.eq('unresolved_form').to_numpy(),'ST438_eligible_proxy':g.ST438_eligible_proxy.to_numpy(),
               'ST438_four_valid':g.ST438_four_valid.to_numpy()}
        # Candidate domains retain missing respondents in the denominator. An
        # observed administration indicator is NOT a sampling assignment flag.
        candidate_masks={'CBA_standard_intended_candidate':g.audit_mode.eq('CBA_standard').to_numpy(),
            'ST438_observed_admin_candidate':masks['ST438_administered'],
            'ST438_unknown_admin':masks['ST438_unknown'],
            'four_AI_valid':masks['ST438_four_valid'],
            'four_AI_and_critical_valid':masks['ST438_four_valid']&g.ST436Q16DA.isin([1,2,3,4]).to_numpy()}
        for group,mask in candidate_masks.items():
            ng,wg=count(mask,w)
            eligibility.append({**base,'candidate_domain':group,'N':ng,'weighted_N':wg,'weighted_pct_total':100*wg/total,
                                'coverage_75_pass':100*wg/total>=75.,'status':'candidate only; no modelling or silent exclusions'})
        nn,ww=count(masks['UH'],w)
        uhrows.append({**base,'Option_UH_country':int(g.Option_UH.iloc[0]),'Option_UH_conflict':bool(nn>0 and g.Option_UH.iloc[0]!=1),'N_UH':nn,'weighted_N_UH':ww,'weighted_pct_UH':100*ww/total})
        means={}
        for group,mask in masks.items():
            ng,wg=count(mask,w)
            for d in DOMAINS:
                estimates=[];denoms=[];counts=[]
                for m in range(1,11):
                    x=g[f'PV{m}{d}'].to_numpy();ok=mask&np.isfinite(x);npv,wpv=count(ok,w)
                    mu=float(np.dot(w[ok],x[ok])/wpv) if wpv>0 else np.nan
                    estimates.append(mu);denoms.append(wpv);counts.append(npv)
                    perpv.append({**base,'group':group,'domain':d,'PV':m,'N_PV_valid':npv,'weighted_N_PV_valid':wpv,'mean':mu})
                estimates=np.array(estimates);allpv=np.isfinite(estimates).all()
                mu=float(estimates.mean()) if allpv else np.nan
                means[(group,d)]=estimates
                perf.append({**base,'group':group,'domain':d,'N_group':ng,'weighted_N_group':wg,'weighted_pct_group':100*wg/total,
                             'N_PV_valid_min':min(counts),'weighted_N_PV_valid_min':min(denoms),'PV_count':int(np.isfinite(estimates).sum()),
                             'mean_10PV':mu,'PV_estimates_sd_not_SE':float(estimates.std(ddof=1)) if allpv else np.nan,
                             'SE':np.nan,'SE_status':'not estimated: numeric 2025 Fay factor unconfirmed','small_group_N_lt_30':ng<30})
        for a,b in [('ST438_administered','ST438_not_administered'),('CBA','PBA'),('UH','CBA_standard'),('ST438_four_valid','ST438_administered')]:
            for d in DOMAINS:
                diff=means[(a,d)]-means[(b,d)]
                contrasts.append({**base,'group_A':a,'group_B':b,'domain':d,'difference_A_minus_B':diff.mean() if np.isfinite(diff).all() else np.nan,
                                  'N_A':int(masks[a].sum()),'N_B':int(masks[b].sum()),'interpretation':'descriptive selection contrast; not causal; no inferential SE'})
    coverage=pd.DataFrame(coverage);senate=pd.DataFrame(senate)
    write(coverage,'ai_coverage_by_country.csv');write(pd.DataFrame(modes),'administration_mode_by_country.csv')
    write(senate,'senate_weight_audit.csv');write(pd.DataFrame(patterns),'st438_administration_patterns.csv')
    write(pd.DataFrame(uhrows),'une_heure_by_country.csv');write(pd.DataFrame(uhrows).query('OECD==1'),'une_heure_oecd.csv')
    write(pd.DataFrame(perf),'selection_performance_by_country.csv');write(pd.DataFrame(perpv),'selection_performance_by_pv.csv')
    write(pd.DataFrame(contrasts),'selection_performance_contrasts.csv')
    write(pd.DataFrame(eligibility),'selection_candidate_domains.csv')
    bookrows=raw.groupby(['CNT','ADMINMODE','BOOKID','Option_UH','audit_mode','ST438_status'],dropna=False).agg(N=('W_FSTUWT','size'),weighted_N=('W_FSTUWT','sum')).reset_index()
    write(bookrows,'book_mode_questionnaire_crosscheck.csv')
    fail=coverage.loc[~coverage.coverage_75_pass,['country','country_name','OECD','variable','weighted_pct_valid','weighted_pct_structural_not_administered','weighted_pct_no_response']]
    write(fail,'coverage_75_failures.csv')
    summary={'rows':len(raw),'countries':raw.CNT.nunique(),'OECD_countries':raw.loc[raw.OECD.eq(1),'CNT'].nunique(),
             'SENWT_all_formula_pass':bool(senate.allclose.all()),'SENWT_all_sum_pass':bool(senate.sum_5000_pass.all()),
             'SENWT_max_relative_difference':senate.max_relative_difference.max(),
             'classification_counts':raw.audit_mode.value_counts().to_dict(),'ST438_status_counts':raw.ST438_status.value_counts().to_dict(),
             'OECD_failures_by_variable':fail.query('OECD==1').groupby('variable').country.apply(list).to_dict(),
             'all_failures_by_variable':fail.groupby('variable').country.apply(list).to_dict(),
             'unexpected_codes_total':int(coverage.N_unexpected_code.sum()),'regressions_executed':False,'Fay_numeric_2025_confirmed':False}
    save_json('results/selection_audit_summary.json',summary)
    print(summary,flush=True)
    print(pd.DataFrame(uhrows).query('OECD==1').sort_values('weighted_pct_UH',ascending=False).head(12).to_string(index=False),flush=True)
    log('ETAPA 2A: cobertura, modalidades y contrastes descriptivos 10 PV',str(summary),'Publicar todos los países y flags del 75%; mantener M1–M5 sin ejecutar','Constante numérica Fay 2025 no confirmada; contrastes sin SE')

if __name__=='__main__':main()
