"""Portable orchestration around preserved statistical implementations."""
from pathlib import Path
import os,sys,json,shutil,subprocess,hashlib,argparse,time,zlib
REPO=Path(__file__).resolve().parents[1]
RUN=Path(os.environ.get('PISA_RUN_ROOT',str(REPO/'.reproduction/outputs'))).resolve()
FIX=REPO/'scripts/fixtures'
EXPECTED=json.loads((FIX/'expected_dimensions.json').read_text())
SEQUENCES={
 'prepare':['03_build_subset.py','2a_extract_audit_data.py'],
 'selection':['2a_selection_audit.py','@compendium','2a_generate_report.py','2a_check_audit.py'],
 'validation':['2b_validate_fay.py'],
 'main':['2b_national_models.py','2b_synthesize.py','2b_check_results.py','2c_prepare.py','2c_models.py'],
 'diagnostics':['2c_diagnostics.py','2c_support_augment.py'],
 'digital':['2c_digital_matched.py','2c_task_comparators.py','2c_comparison_summaries.py'],
 'synthesis':['2c_synthesize.py'],
 'verify':['2c_verify.py','@expected'],
 'figures':['2b_figures.py','2c_figures.py'],
 'report':['2c_report.py']}
def environment():
    import importlib.metadata
    modules=['numpy','pandas','pyreadstat','pyarrow','scipy','openpyxl','zipfile_deflate64','pypdf','matplotlib']
    for module in modules:__import__(module)
    print('Python',sys.version.split()[0],'; scientific dependencies available',flush=True)
    return True
def initialize():
    for d in ['scripts','results','figures','report','data/raw','data/processed','data/documentation']:(RUN/d).mkdir(parents=True,exist_ok=True)
    for p in (REPO/'scripts/legacy').glob('*.py'):shutil.copyfile(p,RUN/'scripts'/p.name)
    shutil.copyfile(FIX/'codebook_country_labels.json',RUN/'data/documentation/codebook_parsed.json')
    shutil.copyfile(FIX/'official_fay_reference.csv',RUN/'data/documentation/official_fay_reference.csv')
    shutil.copyfile(REPO/'docs/VARIABLE_DICTIONARY.csv',RUN/'results/variable_dictionary.csv')
    for name in ['STAGE_2B_PLAN.md','STAGE_2C_PLAN.md']:
        shutil.copyfile(REPO/'docs/history'/name,RUN/name)
    (RUN/'results/stage2b_status.json').write_text(json.dumps({'status':'PENDING','restricted_estimand':True}))
def extract_and_metadata(puf=None):
    import zipfile_deflate64,zipfile,pyreadstat
    archive=Path(puf or REPO/'data/raw/CY09_MS_STU_PUF.zip').resolve()
    if not archive.is_file():
        raise SystemExit('Missing original CY09_MS_STU_PUF.zip. Download the Student SPSS PUF from https://www.oecd.org/en/data/datasets/pisa-2025-database.html (PISA data > Download datasets). Place in data/raw/ or pass --puf /path/to/ZIP. No data are downloaded automatically.')
    h=hashlib.sha256()
    with archive.open('rb') as f:
        for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
    if h.hexdigest()!=EXPECTED['zip_sha256']:raise SystemExit('PUF SHA256 differs from the studied release. Stop; do not silently analyse a revised PUF.')
    raw=RUN.parent/'work/raw';raw.mkdir(parents=True,exist_ok=True)
    sav=raw/'CY09_MS_STU_PUF.sav'
    print('Validated original ZIP; extracting 2.17 GB locally (Deflate64/CRC)',flush=True)
    with zipfile.ZipFile(archive) as z:
        info=z.getinfo(sav.name)
        assert info.file_size==EXPECTED['sav_bytes'] and f'{info.CRC:08x}'==EXPECTED['sav_crc32']
        # zipfile-deflate64 patches method 9; streaming to the specified file avoids path traversal.
        with z.open(info) as inp,sav.open('wb') as out:shutil.copyfileobj(inp,out,8*1024*1024)
    assert sav.stat().st_size==EXPECTED['sav_bytes']
    _,meta=pyreadstat.read_sav(str(sav),metadataonly=True,user_missing=True)
    fields=['number_rows','number_columns','file_label','file_encoding','column_names','column_names_to_labels','variable_value_labels','missing_ranges','missing_user_values','original_variable_types','readstat_variable_types','variable_measure','creation_time','modification_time']
    (RUN/'data/processed/stu_metadata.json').write_text(json.dumps({k:getattr(meta,k,None) for k in fields},ensure_ascii=False,default=str),encoding='utf-8')
    assert meta.number_rows==EXPECTED['student_rows'] and meta.number_columns==EXPECTED['student_columns']
    for domain in ['READ','MATH','SCIE']:assert all(f'PV{i}{domain}' in meta.column_names for i in range(1,11))
    assert all(f'W_FSTURWT{i}' in meta.column_names for i in range(1,81))
def compendium():
    import pandas as pd,numpy as np
    reference=pd.read_csv(FIX/'official_st438_reference.csv')
    raw=pd.read_parquet(RUN/'data/processed/selection_audit_raw.parquet',columns=['CNT','W_FSTUWT']+[f'ST438Q0{i}DA' for i in range(1,5)])
    groups={c:g for c,g in raw.groupby('CNT')};computed=[]
    for row in reference.to_dict('records'):
        g=groups[row['country']];v=row['variable'];den=g[v].isin([1,2,3,4,5,99])
        pct=100*g.loc[g[v].eq(row['category']),'W_FSTUWT'].sum()/g.loc[den,'W_FSTUWT'].sum()
        row.update(computed_pct=pct,difference_pp=pct-row['official_pct'],computed_SE=np.nan,SE_validation_status='historical point-only gate; Fay validated in next stage')
        row['pass']=abs(row['difference_pp'])<=row['tolerance_pp'];computed.append(row)
    result=pd.DataFrame(computed);assert len(result)==1680 and result['pass'].all()
    result.to_csv(RUN/'results/official_validation.csv',index=False,encoding='utf-8-sig')
def expected_check():
    import pandas as pd,numpy as np
    locations=json.loads((FIX/'result_locations.json').read_text());checks=[]
    for name in ['stage2c_all_national_models.csv','stage2c_equal_weight_summary.csv','country_effects_M1.csv','country_effects_M2.csv',
                 'domain_specificity_tests.csv','model_progression_same_sample.csv','digital_comparison_same_sample_summary.csv','fay2025_validation.csv']:
        actual=pd.read_csv(RUN/'results'/name);reference=pd.read_csv(REPO/locations[name])
        assert len(actual)==len(reference),(name,'row count mismatch')
        numeric=['beta','SE','q_FDR','computed_mean','computed_SE','A_to_C_total','SE_paired_PV']
        maxerr=0.
        for c in numeric:
            if c in actual and c in reference:
                assert np.allclose(actual[c],reference[c],rtol=1e-9,atol=1e-7,equal_nan=True),(name,c)
                finite=actual[c].notna()&reference[c].notna()
                if finite.any():maxerr=max(maxerr,float(abs(actual.loc[finite,c]-reference.loc[finite,c]).max()))
        checks.append({'file':name,'rows':len(actual),'max_abs_difference':maxerr,'pass':True})
    core=pd.read_csv(RUN/'results/stage2c_equal_weight_summary.csv')
    main=core.loc[core.model.eq('M2-CORE')];assert main.K.eq(32).all()
    assert core.loc[core.model.eq('M2-FULL'),'K'].eq(21).all()
    assert all(not {'USA','ISR'}&set(c.split(';')) for c in main.countries)
    (RUN/'results/public_reproduction_check.json').write_text(json.dumps({'status':'PASS','checks':checks,'CORE_K':32,'FULL_K':21,'M':10,'R':80,'fay':.5},indent=2))
    print('Public-reference reproduction checks PASS',flush=True)
def run_script(name):
    if name=='@compendium':return compendium()
    if name=='@expected':return expected_check()
    env=os.environ.copy();env['PISA_RUN_ROOT']=str(RUN);env['OPENBLAS_NUM_THREADS']='2'
    env['MKL_NUM_THREADS']='2';env['OMP_NUM_THREADS']='2';env['PYTHONIOENCODING']='utf-8'
    print('Running',name,flush=True)
    subprocess.run([sys.executable,str(RUN/'scripts'/name)],env=env,cwd=RUN,check=True)
def main(default='all'):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--stage',choices=['all']+list(SEQUENCES),default=default);parser.add_argument('--puf');args=parser.parse_args()
    environment();start=time.time()
    if args.stage in ['all','prepare']:
        initialize();extract_and_metadata(args.puf)
    else:
        # Refresh executable code while preserving data/status needed by the chosen stage.
        for p in (REPO/'scripts/legacy').glob('*.py'):shutil.copyfile(p,RUN/'scripts'/p.name)
    stages=list(SEQUENCES) if args.stage=='all' else [args.stage]
    for stage in stages:
        for script in SEQUENCES[stage]:run_script(script)
    print(f'Completed {args.stage}; elapsed {time.time()-start:.1f}s. Outputs in {RUN}',flush=True)
if __name__=='__main__':main()
