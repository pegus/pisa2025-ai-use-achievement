"""Select only verified columns; audit user-missing before replacing with nulls."""
import re, json, csv, importlib.metadata, platform, time
from common import ROOT, load_json, save_json, log
import numpy as np
import pandas as pd
import pyreadstat

AI = [f'ST438Q0{i}DA' for i in range(1,5)]
BASE = ['CNT','CNTRYID','CNTSCHID','CNTSTUID','OECD','ADMINMODE','STRATUM','SUBNATIO','BOOKID','LANGTEST_COG','LANGTEST_QQQ','Option_ICTQ','Option_UH','SENWT',
        'AIUSESCH', 'ST436Q02DA','ST436Q16DA','ESCS','AGE','IMMIG','ST004D01T','ST022Q01TA',
        'ICTRES','ICTSCH','ICTHOME','ICTQUAL','ST097Q06DA',
        'ST250Q02JA','ST250Q03JA','ST250Q04JA','ST250Q05JA',
        'ST326Q01JA','ST326Q02JA','ST326Q03JA','ST326Q04JA','ST326Q05JA','ST326Q06JA',
        'IC170Q10DA','IC171Q10DA','IC182Q05DA', 'SELFREG'] + AI

def missing_codes(labels):
    p=re.compile(r'valid skip|system missing|not administered|not applicable|invalid|no response|not reached|omitted',re.I)
    return {str(k):v for k,v in labels.items() if p.search(v or '')}

def audit(df, meta, columns):
    rows=[]
    w=df.W_FSTUWT
    grouped=df.groupby('CNT',observed=True).indices
    groups=[('ALL',np.arange(len(df)))]+list(grouped.items())
    for name in columns:
        if name.startswith('W_') or re.fullmatch(r'PV\d+(READ|MATH|SCIE)',name): continue
        raw=df[name]
        special=missing_codes(meta.variable_value_labels.get(name,{}))
        bad=raw.isna().to_numpy().copy()
        categories={}
        for val, label in special.items():
            code=float(val) if pd.api.types.is_numeric_dtype(raw) else str(val)
            mask=raw.eq(code).to_numpy()
            categories[val]=(label,mask)
            bad |= mask
        # Include SPSS ranges even if label absent.
        for ran in meta.missing_ranges.get(name,[]):
            if pd.api.types.is_numeric_dtype(raw): bad |= raw.between(ran['lo'],ran['hi']).to_numpy()
        for country, idx in groups:
            total=len(idx); valid=~bad[idx]; weights=w.iloc[idx].to_numpy()
            row={'country':country,'variable':name,'N_total':total,'N_valid':int(valid.sum()),'N_missing':int((~valid).sum()),
                 'pct_valid_unweighted':100*valid.mean(),'pct_missing_unweighted':100*(~valid).mean(),
                 'weighted_total':float(weights.sum()),'weighted_valid':float(weights[valid].sum()),
                 'pct_valid_population_weighted':100*weights[valid].sum()/weights.sum(),
                 'N_system_null':int(raw.iloc[idx].isna().sum()),
                 'missing_code_counts_json':json.dumps({val:{'label':lab,'N':int(mask[idx].sum()),'weighted_N':float(weights[mask[idx]].sum())} for val,(lab,mask) in categories.items() if mask[idx].any()},ensure_ascii=False)}
            rows.append(row)
        df.loc[bad,name]=np.nan if pd.api.types.is_numeric_dtype(raw) else None
    result=pd.DataFrame(rows)
    result[result.country=='ALL'].drop(columns='country').to_csv(ROOT/'results/missingness_by_variable.csv',index=False,encoding='utf-8-sig')
    result[result.country!='ALL'].to_csv(ROOT/'results/missingness_by_country.csv',index=False,encoding='utf-8-sig')

def main():
    metadata=load_json('data/processed/stu_metadata.json')
    names=metadata['column_names']
    mandatory=AI+['AIUSESCH','CNT','CNTSCHID','CNTSTUID','OECD','W_FSTUWT','ESCS']
    mandatory += [f'W_FSTURWT{i}' for i in range(1,81)]
    mandatory += [f'PV{i}{domain}' for domain in ['READ','MATH','SCIE'] for i in range(1,11)]
    absent=[n for n in mandatory if n not in names]
    if absent: raise RuntimeError(f'Mandatory variables absent: {absent}')
    cols=list(dict.fromkeys([n for n in BASE+mandatory if n in names]))
    save_json('data/processed/selected_columns.json',cols)
    print(f'Reading {len(cols)}/{len(names)} columns, preserving all rows',flush=True)
    start=time.time()
    df,meta=pyreadstat.read_sav(str(ROOT.parent/'work/raw/CY09_MS_STU_PUF.sav'),usecols=cols,user_missing=True,apply_value_formats=False)
    print('Loaded',df.shape,'RAM dataframe MiB',round(df.memory_usage(deep=True).sum()/1024**2,1),'seconds',round(time.time()-start,1),flush=True)
    if len(df)!=metadata['number_rows']: raise RuntimeError('Row count mismatch')
    if df.duplicated(['CNT','CNTSTUID']).any(): raise RuntimeError('Student key is not unique')
    if df.OECD.isna().any() or not set(df.OECD.unique()) <= {0,1}: raise RuntimeError('Invalid OECD flag')
    if not df.groupby('CNT',observed=True).OECD.nunique().eq(1).all(): raise RuntimeError('OECD flag inconsistent within country')
    if not np.isfinite(df.W_FSTUWT).all() or not df.W_FSTUWT.gt(0).all(): raise RuntimeError('Invalid final weights')
    audit(df,meta,cols)
    df.to_parquet(ROOT/'data/processed/pisa2025_ai_subset.parquet',index=False,compression='zstd')
    coverage=[]
    for country,g in df.groupby('CNT',observed=True):
        record={'country':country,'OECD':int(g.OECD.iloc[0]),'N':len(g),'population_weight_sum':g.W_FSTUWT.sum(), 'N_schools':g.CNTSCHID.nunique()}
        for n in AI+['AIUSESCH','ST436Q16DA']:
            record[n+'_N_valid']=int(g[n].notna().sum());record[n+'_pct_valid']=100*g[n].notna().mean()
        coverage.append(record)
    pd.DataFrame(coverage).to_csv(ROOT/'results/country_coverage.csv',index=False,encoding='utf-8-sig')
    flow=[{'stage':'All original students','N':len(df)}, {'stage':'OECD original students','N':int(df.OECD.eq(1).sum())}]
    for n in AI:
        flow.append({'stage':'OECD valid '+n,'N':int((df.OECD.eq(1)&df[n].notna()).sum())})
    model2=['ESCS','ST004D01T','AGE','IMMIG','ST022Q01TA']
    for n in AI:
        flow.append({'stage':'OECD complete candidate Model2 '+n,'N':int((df.OECD.eq(1)&df[[n]+model2].notna().all(axis=1)).sum())})
    pd.DataFrame(flow).to_csv(ROOT/'results/sample_flow.csv',index=False)
    # Preserve no student observations from SCH/LDW; only metadata assessed this phase.
    versions={'python':platform.python_version(),'platform':platform.platform(),'packages':{p:importlib.metadata.version(p) for p in ['numpy','pandas','pyreadstat','pyarrow','scipy','openpyxl','zipfile-deflate64','pypdf']}}
    save_json('results/package_versions.json',versions)
    print('N',len(df),'countries',df.CNT.nunique(),'OECD countries',df.loc[df.OECD==1,'CNT'].nunique(),'file MiB',round((ROOT/'data/processed/pisa2025_ai_subset.parquet').stat().st_size/1024**2,1),flush=True)
    log('Dataset reducido y auditoría missing',f'{len(df)} filas, {len(cols)} columnas, {df.CNT.nunique()} países/economías', 'Conservar todos los estudiantes; convertir solo códigos especiales documentados; sin imputación y sin filtrar países aún')

if __name__=='__main__':main()
