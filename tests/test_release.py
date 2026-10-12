"""Checks on public numerical artifacts, plus the statistical kernel on synthetic PVs."""
from pathlib import Path
import unittest,json,sys,importlib.util,tempfile,os
import numpy as np,pandas as pd
REPO=Path(__file__).resolve().parents[1]
def read(category,name):return pd.read_csv(REPO/'results'/category/name)
class ReleaseTests(unittest.TestCase):
    def test_official_fay_validation(self):
        t=read('validation','fay2025_validation.csv')
        self.assertEqual(len(t),18);self.assertTrue(t.PASS.all())
        self.assertTrue(np.allclose(t.k,.5));self.assertTrue(t.replicates.eq(80).all());self.assertTrue(t.plausible_values.eq(10).all())
        self.assertLess(abs(t.computed_mean-t.official_mean).max(),5e-6)
        self.assertLess(abs(t.computed_SE-t.official_SE).max(),5e-6)
        self.assertEqual(set(t.country),{'AUS','COL','DEU','JPN','MEX','TUR'})
    def test_main_estimand(self):
        s=read('aggregated','stage2c_equal_weight_summary.csv');p=s.loc[s.model.eq('M2-CORE')]
        self.assertEqual(len(p),60);self.assertTrue(p.K.eq(32).all())
        self.assertTrue(s.loc[s.model.eq('M2-FULL'),'K'].eq(21).all())
        for c in p.countries:self.assertFalse({'USA','ISR'}&set(c.split(';')))
        n=read('aggregated','M2_core_results.csv');eligible=n.loc[n.primary_synthesis_eligible]
        self.assertGreaterEqual(eligible.joint_coverage_pct.min(),75)
        for row in p.itertuples():
            z=eligible.loc[eligible.domain.eq(row.domain)&eligible.exposure.eq(row.exposure)&eligible.contrast.eq(row.contrast)]
            self.assertEqual(len(z),32);self.assertAlmostEqual(z.beta.mean(),row.beta,places=7)
            self.assertAlmostEqual(np.sqrt((z.SE**2).sum())/32,row.SE,places=7)
    def test_full_reproduction(self):
        t=read('validation','M2_full_reproduction.csv');self.assertEqual(len(t),1260)
        self.assertLess(t.abs_beta_difference.max(),1e-8);self.assertLess(t.abs_SE_difference.max(),1e-8)
    def test_expected_pv_and_weight_dimensions(self):
        spec=json.loads((REPO/'scripts/fixtures/expected_dimensions.json').read_text())
        self.assertEqual(spec['M'],10);self.assertEqual(spec['R'],80);self.assertEqual(spec['fay'],.5)
        dictionary=pd.read_csv(REPO/'docs/VARIABLE_DICTIONARY.csv')
        names=set(dictionary.code)
        for d in ['READ','MATH','SCIE']:
            self.assertEqual(len([n for n in names if n.startswith('PV') and n.endswith(d)]),10)
        self.assertTrue(all(f'W_FSTURWT{i}' in names for i in range(1,81)))
    def test_brr_and_pv_combination_analytical(self):
        # Independent scalar calculation with nonzero sampling and imputation variance.
        sys.path.insert(0,str(REPO/'scripts/legacy'))
        spec=importlib.util.spec_from_file_location('kernel',REPO/'scripts/legacy/2b_national_models.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        a=np.zeros((10,81,1));a[:,0,0]=np.arange(10)*2+3
        a[:,1:,0]=a[:,0,0,None]+np.tile([-1.,1.],40)
        q,U,B,T=m.combine(a)
        self.assertAlmostEqual(q[0],12);self.assertAlmostEqual(U[0,0],4)
        self.assertAlmostEqual(B[0,0],np.var(np.arange(10)*2+3,ddof=1))
        self.assertAlmostEqual(T[0,0],4+1.1*np.var(np.arange(10)*2+3,ddof=1))
    def test_no_microdata(self):
        for p in REPO.rglob('*'):
            if not p.is_file() or any(x in p.parts for x in ['.git','.reproduction','.venv','__pycache__']):continue
            self.assertNotIn(p.suffix.lower(),{'.sav','.parquet','.npz','.npy','.sas7bdat','.feather','.dta','.env'})
        for p in (REPO/'results').rglob('*.csv'):
            names=set(pd.read_csv(p,nrows=0).columns.str.upper())
            self.assertFalse(names&{'CNTSTUID','CNTSCHID','STUDENT_ID','SCHOOL_ID'})
if __name__=='__main__':unittest.main()
