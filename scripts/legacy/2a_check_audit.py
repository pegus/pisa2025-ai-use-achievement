"""Independent audit reconciliation, including partition identity for weighted PV means."""
from common import ROOT,load_json,save_json,log
import pandas as pd
import numpy as np
import pyarrow.parquet as pq
import hashlib

def read(name):return pd.read_csv(ROOT/'results'/name)
coverage=read('ai_coverage_by_country.csv')
assert len(coverage)==540 and coverage.country.nunique()==90
assert coverage.loc[coverage.OECD.eq(1),'country'].nunique()==38
assert not coverage.duplicated(['country','variable']).any()
categories=['valid','valid_skip','system_missing_code','structural_not_administered','invalid_response','no_response','system_null','unexpected_code']
assert np.array_equal(coverage[[f'N_{c}' for c in categories]].sum(axis=1),coverage.N_total)
assert np.allclose(coverage[[f'weighted_N_{c}' for c in categories]].sum(axis=1),coverage.weighted_N_total)
assert np.allclose(coverage[[f'weighted_pct_{c}' for c in categories]].sum(axis=1),100)
assert coverage.coverage_75_pass.equals(coverage.weighted_pct_valid.ge(75))
assert coverage.N_unexpected_code.eq(0).all()
for c,g in coverage.groupby('country'):
    assert g.N_total.nunique()==1 and g.weighted_N_total.nunique()==1
    assert g.N_CBA.iloc[0]+g.N_PBA.iloc[0]+g.N_ADMINMODE_other.iloc[0]+g.N_ADMINMODE_missing.iloc[0]==g.N_total.iloc[0]
senate=read('senate_weight_audit.csv')
assert senate.allclose.all() and senate.sum_5000_pass.all()
subset=ROOT/'data/processed/pisa2025_ai_subset.parquet'
assert len(pq.read_schema(subset))==156 and 'SENWT' in pq.read_schema(subset).names
small=pd.read_parquet(subset,columns=['CNT','CNTSTUID','SENWT','Option_UH'])
raw=pd.read_parquet(ROOT/'data/processed/selection_audit_raw.parquet',columns=['CNT','CNTSTUID','SENWT','Option_UH'])
assert small.equals(raw) and len(small)==755721 and not small.duplicated(['CNT','CNTSTUID']).any()
mode=read('administration_mode_by_country.csv')
form=mode.loc[mode.classification.eq('validated_form')]
assert form.groupby('country').N.sum().equals(coverage.drop_duplicates('country').set_index('country').N_total)
uh=read('une_heure_oecd.csv')
assert len(uh)==38 and uh.loc[uh.country.eq('CRI'),'Option_UH_conflict'].item()
assert uh.N_UH.sum()==int(form.loc[form.OECD.eq(1)&form['mode'].eq('UH'),'N'].sum())
pv=read('selection_performance_by_pv.csv')
# ALL must reconcile with disjoint questionnaire-administration groups separately
# for each PV/domain, including item system missing and unadministered students.
parts=['ST438_administered','ST438_not_administered','ST438_mixed_structural','ST438_unknown']
part=pv.loc[pv.group.isin(parts)].copy()
part['numerator']=part['mean'].fillna(0)*part.weighted_N_PV_valid
sums=part.groupby(['country','domain','PV'])[['numerator','weighted_N_PV_valid','N_PV_valid']].sum()
whole=pv.loc[pv.group.eq('ALL')].set_index(['country','domain','PV']).sort_index()
assert np.array_equal(sums.N_PV_valid,whole.N_PV_valid)
assert np.allclose(sums.weighted_N_PV_valid,whole.weighted_N_PV_valid,rtol=1e-9)
assert np.allclose(sums.numerator/sums.weighted_N_PV_valid,whole['mean'],rtol=1e-9,equal_nan=True)
performance=read('selection_performance_by_country.csv')
pooled=pv.groupby(['country','group','domain'])['mean'].agg(['mean','count'])
target=performance.set_index(['country','group','domain']).sort_index()
assert np.allclose(pooled['mean'],target.mean_10PV,equal_nan=True,rtol=1e-9)
assert np.array_equal(pooled['count'],target.PV_count)
assert target.SE.isna().all()
contrasts=read('selection_performance_contrasts.csv')
assert contrasts.loc[contrasts.group_A.eq('CBA')&contrasts.group_B.eq('PBA'),'difference_A_minus_B'].isna().all()
official=read('selection_official_reproduction.csv')
assert len(official)>=2 and official['pass'].all()
full=read('official_validation.csv');assert len(full)==1680 and full['pass'].all()
summary=load_json('results/selection_audit_summary.json')
assert summary['decision']=='STOP' and not summary['M1_M5_executed'] and not summary['Fay_numeric_2025_confirmed']
report=(ROOT/'results/selection_audit.md').read_text(encoding='utf-8')
assert '**Conclusión operativa: STOP.' in report
paths=['results/selection_audit.md','results/ai_coverage_by_country.csv','results/selection_official_reproduction.csv','results/selection_performance_by_country.csv']
hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
status={'data_checks':'PASS','audit_decision':'STOP','coverage_rows':540,'student_rows':755721,'subset_columns':156,
        'countries':90,'OECD_countries':38,'official_ST438_checks':1680,'official_example_checks':len(official),
        'coverage_partitions_reconcile':True,'PV_partition_means_reconcile':True,'SENWT_formula_pass':True,
        'CBA_PBA_within_country_contrasts':'not identifiable; all NA','inference':'NOT_EXECUTED','sha256':hashes}
save_json('results/selection_audit_quality_checks.json',status)
log('Reconciliación independiente ETAPA 2A',str(status),'Comprobaciones de datos PASS; decisión científica STOP sin ejecutar modelos')
print(status,flush=True)
