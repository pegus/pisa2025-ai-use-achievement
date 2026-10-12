"""Read only audit columns, retain exact SPSS user-missing values."""
from common import ROOT,load_json,save_json,log
import pyreadstat
import pandas as pd
import numpy as np

AI=[f'ST438Q0{i}DA' for i in range(1,5)]
columns=['CNT','CNTRYID','CNTSCHID','CNTSTUID','OECD','ADMINMODE','BOOKID','Option_UH','SENWT','W_FSTUWT','AIUSESCH','ST436Q16DA']+AI
columns += [f'PV{i}{d}' for d in ['READ','MATH','SCIE'] for i in range(1,11)]
raw,meta=pyreadstat.read_sav(str(ROOT.parent/'work/raw/CY09_MS_STU_PUF.sav'),usecols=columns,user_missing=True)
assert len(raw)==755721 and not raw.duplicated(['CNT','CNTSTUID']).any()
rawpath=ROOT/'data/processed/selection_audit_raw.parquet'
raw.to_parquet(rawpath,index=False,compression='zstd')
path=ROOT/'data/processed/pisa2025_ai_subset.parquet'
subset=pd.read_parquet(path)
keys=['CNT','CNTSTUID']
assert subset[keys].equals(raw[keys])
for name in ['SENWT','Option_UH']:
    subset[name]=raw[name].to_numpy()
    assert name in meta.column_names
temporary=path.with_suffix('.partial.parquet')
subset.to_parquet(temporary,index=False,compression='zstd');temporary.replace(path)
selected=load_json('data/processed/selected_columns.json')
save_json('data/processed/selected_columns.json',list(dict.fromkeys(selected+['SENWT','Option_UH'])))
print('raw',raw.shape,'subset',subset.shape,flush=True)
print('labels',{n:meta.column_names_to_labels[n] for n in ['SENWT','Option_UH']},flush=True)
print('UH option values',meta.variable_value_labels.get('Option_UH'),flush=True)
print('book by mode',raw.groupby(['BOOKID','ADMINMODE'],dropna=False).size().to_dict(),flush=True)
print('UH option by country variation',raw.groupby('CNT').Option_UH.nunique().value_counts().to_dict(),flush=True)
log('Extracción selectiva ETAPA 2A y SENWT',f'Archivo de auditoría {raw.shape}; reducido {subset.shape}','Conservar códigos crudos solo en archivo de auditoría; añadir SENWT y Option_UH al reducido con llaves verificadas')
