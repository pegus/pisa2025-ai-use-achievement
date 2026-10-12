"""Independent QR school-dummy and within checks, plus result reconciliation."""
import os
os.environ['OPENBLAS_NUM_THREADS']='2'
from common import ROOT,load_json,save_json
import numpy as np,pandas as pd
from scipy.linalg import lstsq
from scipy.stats import false_discovery_control
from importlib.util import spec_from_file_location,module_from_spec
sp=spec_from_file_location('models',ROOT/'scripts/2c_models.py');m=module_from_spec(sp);sp.loader.exec_module(m)
def explicit_check(sub,exposure,controls,domain,pv,r,theta):
    X,terms,_=m.design(sub,[exposure],controls,True);codes,schools=pd.factorize(sub.CNTSCHID,sort=True)
    # Exhaustive school indicators, no intercept: mathematically equivalent.
    dummy=np.eye(len(schools))[codes];xx=np.column_stack([X,dummy]);w=sub[m.WEIGHTS[r]].to_numpy(float);w=w/w.mean()
    y=sub[f'PV{pv}{domain}'].to_numpy(float);sqrtw=np.sqrt(w)
    coef,_,_,_=lstsq(xx*sqrtw[:,None],y*sqrtw,lapack_driver='gelsy')
    expected=theta[m.DOM.index(domain),pv-1,r,0,:]
    return float(np.max(np.abs(coef[:4]-expected)))
def synthetic_check():
    rng=np.random.default_rng(52025);n=180;school=np.repeat(np.arange(12),15);ai=rng.integers(1,6,n);x=rng.normal(size=n)
    columns={'CNTSCHID':school,'ST438Q01DA':ai,'ESCS':x,'IMMIG':np.ones(n),'ST022Q01TA':np.ones(n)}
    weights=rng.lognormal(0,.5,(n,81))
    for r,v in enumerate(m.WEIGHTS):columns[v]=weights[:,r]
    for d in m.DOM:
        for pv in range(1,11):columns[f'PV{pv}{d}']=400+7*ai+12*x+25*school+rng.normal(0,5,n)
    sub=pd.DataFrame(columns)
    X,terms,_=m.design(sub,['ST438Q01DA'],m.CORE,True);theta,info=m.fit_arrays(sub,X,terms,True)
    assert theta is not None
    # Data intentionally have different within-school weight ratios per replica.
    errors=[];wrong_errors=[]
    codes,schools=pd.factorize(sub.CNTSCHID);Y=sub.PV1READ.to_numpy();w0=weights[:,0]
    xmean=np.stack([np.average(X[codes==s],weights=w0[codes==s],axis=0) for s in range(len(schools))]);ymean=np.array([np.average(Y[codes==s],weights=w0[codes==s]) for s in range(len(schools))])
    fixedX=X-xmean[codes];fixedY=Y-ymean[codes]
    for r in [0,1,17,80]:
        err=explicit_check(sub,'ST438Q01DA',m.CORE,'READ',1,r,theta[:,:,:,None,:4]);errors.append(err)
        w=weights[:,r];wrong=lstsq(fixedX*np.sqrt(w)[:,None],fixedY*np.sqrt(w),lapack_driver='gelsy')[0]
        wrong_errors.append(float(np.max(abs(wrong[:4]-theta[0,0,r,:4]))))
    assert max(errors)<1e-8 and max(wrong_errors)>1e-3
    return {'max_abs_error_correct_absorption':max(errors),'max_error_reusing_final_weight_transformation':max(wrong_errors),'deliberately_nonproportional_within_school_replica_weights':True}
def main():
    independent=[];data=pd.read_parquet(ROOT/'data/processed/pisa2025_stage2c_oecd.parquet')
    for country,exposure,base,controls in [('AUT','ST438Q01DA','CORE',m.CORE),('MEX','ST438Q03DA','FULL',m.FULL),('FRA','ST438Q04DA','CORE',m.CORE)]:
        g=data.loc[data.CNT.eq(country)];sub=g.loc[m.make_mask(g,[exposure],controls,True)]
        theta=np.load(m.SAVE/f'{country}__M2-SCHOOL-FE__{base}__{exposure}.npz')['theta']
        for r,pv in [(0,1),(17,7),(80,2)]:
            err=explicit_check(sub,exposure,controls,'READ',pv,r,theta)
            assert err<1e-7,(country,r,err)
            independent.append({'country':country,'exposure':exposure,'base_controls':base,'domain':'READ','PV':pv,'replica':r,'max_abs_beta_difference':err,'method':'independent QR with explicit full school indicators','pass':True})
    m.write(pd.DataFrame(independent),'school_FE_independent_checks.csv')
    synth=synthetic_check()
    summary=pd.read_csv(ROOT/'results/stage2c_equal_weight_summary.csv');df=pd.read_csv(ROOT/'results/stage2c_all_national_models.csv')
    max_summary=0
    for (model,base),g in summary.groupby(['model','base_controls']):
        ok=g.p_raw.notna();expected=false_discovery_control(g.loc[ok,'p_raw'].to_numpy())
        assert np.max(abs(expected-g.loc[ok,'q_FDR']))<1e-9
        for row in g.to_dict('records'):
            d=df.loc[df.model.eq(model)&df.base_controls.eq(base)&df.exposure.eq(row['exposure'])&df.domain.eq(row['domain'])&df.contrast.eq(row['contrast'])&df.primary_synthesis_eligible]
            assert len(d)==row['K']
            if len(d):
                err=abs(d.beta.mean()-row['beta']);max_summary=max(max_summary,err)
                assert err<1e-8 and abs(np.sqrt((d.SE**2).sum())/len(d)-row['SE'])<1e-8
    assert np.allclose(df.loc[df.fit_status.eq('estimated'),'SE']**2,df.loc[df.fit_status.eq('estimated'),'sampling_variance']+1.1*df.loc[df.fit_status.eq('estimated'),'between_PV_variance'],rtol=1e-9,atol=1e-8)
    assert not set(df.country)&{'ISR','USA'}
    assert df.loc[df.primary_synthesis_eligible,'joint_coverage_pct'].min()>=75
    assert df.loc[df.fit_status.ne('estimated'),'beta'].isna().all()
    dom=pd.read_csv(ROOT/'results/domain_specificity_tests.csv');ok=dom.K.gt(0)
    assert (dom.loc[ok,'SE']+1e-10>=dom.loc[ok,'SE_paired_PV']).all()
    for k,g in dom.groupby(['model','base_controls']):
        ok=g.p_raw.notna();assert np.allclose(false_discovery_control(g.loc[ok,'p_raw'].to_numpy()),g.loc[ok,'q_FDR_16'])
    full=pd.read_csv(ROOT/'results/M2_full_reproduction.csv');assert len(full)==1260
    prog=pd.read_csv(ROOT/'results/model_progression_same_sample.csv')
    assert len(prog)==60 and prog.A_M1_36_K.eq(36).all() and prog.B_M1_21_K.eq(21).all() and prog.E_M2_FULL_21_K.eq(21).all()
    components=prog.A_to_C_country_component+prog.A_to_C_student_selection_component+prog.A_to_C_controls_same_students_component
    assert np.max(abs(components-prog.A_to_C_total))<1e-8
    summary_status={'status':'PASS','full_M2_reproduction_rows':len(full),'max_full_beta_error':full.abs_beta_difference.max(),'max_full_SE_error':full.abs_SE_difference.max(),
       'independent_real_school_dummy_QR_checks':len(independent),'max_QR_error':max(r['max_abs_beta_difference'] for r in independent),
       'synthetic_replica_absorption_check':synth,'max_equal_country_summary_error':max_summary,'FDR_independent_scipy_check':'PASS',
       'coverage_missing_and_country_flags':'PASS','domain_conservative_bound_vs_paired':'PASS','progression_exact_decomposition':'PASS','LDW':False}
    save_json('results/stage2c_quality_checks.json',summary_status)
    print(summary_status,flush=True)
if __name__=='__main__':main()
