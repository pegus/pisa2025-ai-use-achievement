"""Independent numerical verification and country/coverage/FDR reconciliation."""
from common import ROOT,load_json,save_json,log
import numpy as np
import pandas as pd
from scipy.linalg import lstsq
from scipy.stats import false_discovery_control
from pathlib import Path
import hashlib

def read(p):return pd.read_csv(ROOT/'results'/p)
assert load_json('results/fay2025_validation_status.json')['passed']==18
fay=read('fay2025_validation.csv');assert fay.PASS.all() and fay.SE_pass.all()
cov=read('model_joint_coverage.csv')
assert len(cov)==38*4*3*4 and not cov.duplicated(['country','exposure','domain','model']).any()
assert cov.below_75_joint_coverage.equals(cov.joint_linkage_pct.lt(75))
assert not cov.loc[cov.model.isin(['M3','M5']),'fit_authorized_this_stage'].any()
elig=read('stage2b_country_eligibility.csv');assert elig.ST438_all_four_75_pass.sum()==36 and elig.H6_item_75_pass.sum()==32
summary=read('primary_contrasts_M2.csv');assert len(summary)==60 and not summary.duplicated(['exposure','domain','contrast']).any()
assert np.allclose(false_discovery_control(summary.p_raw.to_numpy(),method='bh'),summary.q_FDR,rtol=1e-9,atol=1e-300)
countries=read('country_effects_M2.csv')
assert set(countries.country)==set(elig.loc[elig.ST438_all_four_75_pass,'country'])
assert len(countries)==36*4*3*5
for r in summary.itertuples():
    g=countries.loc[countries.exposure.eq(r.exposure)&countries.domain.eq(r.domain)&countries.contrast.eq(r.contrast)&countries.fit_status.eq('estimated')&countries.primary_synthesis_eligible]
    assert len(g)==r.K and np.isclose(g.beta.mean(),r.beta,rtol=1e-10,atol=1e-8)
    assert np.isclose((g.SE**2).sum()/len(g)**2,r.SE**2,rtol=1e-10)
    assert r.N==g.N.sum() and np.isclose(r.weighted_N,g.weighted_N.sum(),rtol=1e-10)
    assert not {'ISR','USA'}&set(str(r.countries).split(';'))
    assert np.isclose(r.variance,r.sampling_variance_sum_over_K2+r.between_PV_contribution_sum_over_K2,rtol=1e-10)
missing=countries.loc[countries.fit_status.eq('no_complete_cases')]
assert missing.beta.isna().all() and missing.N.eq(0).all() and missing.joint_coverage_pct.eq(0).all()
explore=read('low_coverage_exploratory_ISR_USA.csv');assert set(explore.country)=={'ISR','USA'} and explore.exploratory_only.all()
sens=read('selection_sensitivity.csv')
a=sens.loc[sens.scenario.eq('A_75')].set_index(['model','exposure','domain','contrast'])
g=sens.loc[sens.scenario.eq('G_all_75')].set_index(['model','exposure','domain','contrast'])
assert np.allclose(a.beta,g.beta) and np.array_equal(a.K,g.K)
assert set(sens.scenario)=={'A_75','B_80','C_85','D_90','E_UH_le_5','F_no_UH_observed','G_all_75'}
assert len(sens)==2*7*60
diagnostics=read('national_fit_diagnostics.csv');assert set(diagnostics.model)=={'M1','M2'}
assert diagnostics.loc[diagnostics.fit_status.eq('estimated'),'max_condition'].lt(1e12).all()

# Independent SVD-based weighted least-squares checks use raw, uncentred
# covariates rather than the batch normal-equation implementation.
cols=['CNT','W_FSTUWT','W_FSTURWT17','W_FSTURWT80','ESCS','ST004D01T','AGE','IMMIG','ST022Q01TA',
      'ST438Q01DA','ST438Q03DA','ST438Q04DA','PV2READ','PV2MATH','PV2SCIE']
data=pd.read_parquet(ROOT/'data/processed/pisa2025_ai_subset.parquet',columns=cols)
checks=[]
for c,e,d in [('AUT','ST438Q01DA','READ'),('MEX','ST438Q03DA','MATH'),('FRA','ST438Q04DA','SCIE')]:
    required=[e,'ESCS','ST004D01T','AGE','IMMIG','ST022Q01TA',f'PV2{d}'];sub=data.loc[data.CNT.eq(c)&data[required].notna().all(axis=1)]
    x=[np.ones(len(sub))]+[sub[e].eq(k).to_numpy(dtype=float) for k in [2,3,4,5]]
    for arr in [sub.ESCS.to_numpy(),sub.ST004D01T.eq(2).to_numpy(dtype=float),sub.AGE.to_numpy(),
                sub.IMMIG.eq(2).to_numpy(dtype=float),sub.IMMIG.eq(3).to_numpy(dtype=float),sub.ST022Q01TA.eq(2).to_numpy(dtype=float)]:
        if np.ptp(arr)>0:x.append(arr)
    X=np.column_stack(x);y=sub[f'PV2{d}'].to_numpy()
    arr=np.load(ROOT/f'data/processed/stage2b_model_estimates/{c}_{e}_{d}_M2.npz')['theta']
    for name,index in [('W_FSTUWT',0),('W_FSTURWT17',17),('W_FSTURWT80',80)]:
        sqrt=np.sqrt(sub[name].to_numpy());beta=lstsq(sqrt[:,None]*X,sqrt*y,lapack_driver='gelsd')[0]
        error=float(np.max(np.abs(beta[1:5]-arr[1,index,1:5])));assert error<1e-8
        checks.append({'country':c,'exposure':e,'domain':d,'PV':2,'weight':name,'max_AI_coefficient_difference':error,'PASS':True})
pd.DataFrame(checks).to_csv(ROOT/'results/independent_WLS_checks.csv',index=False,encoding='utf-8-sig')
files=['fay2025_validation.csv','model_joint_coverage.csv','descriptives_M0.csv','country_effects_M1.csv','country_effects_M2.csv',
       'oecd_equal_weight_summary_M2.csv','primary_contrasts_M2.csv','selection_sensitivity.csv','low_coverage_exploratory_ISR_USA.csv']
assert all((ROOT/'results'/p).stat().st_size>0 for p in files)
status={'data_and_numerical_checks':'PASS','Fay_checks':18,'independent_SVD_WLS_checks':len(checks),
        'max_SVD_coefficient_difference':max(c['max_AI_coefficient_difference'] for c in checks),
        'primary_FDR_family_size':60,'models_fitted':['M1','M2'],'M0_descriptives':True,'M3_M4_M5_LDW_fitted':False,
        'candidate_ST438_K':36,'candidate_H6_K':32,'primary_M2_K':sorted(summary.K.unique().tolist()),
        'no_complete_case_country_codes':sorted(missing.country.unique().tolist()),
        'SHA256':{p:hashlib.sha256((ROOT/'results'/p).read_bytes()).hexdigest() for p in files}}
save_json('results/stage2b_quality_checks.json',status)
log('Control independiente ETAPA 2B',str(status),'Datos/varianza/SVD/FDR y exclusiones conciliados; solo M0/M1/M2')
print(status,flush=True)
