"""Only population mean/SE validation. No AI regression until the gate passes."""
from common import ROOT,load_json,save_json,log
import numpy as np
import pandas as pd
import openpyxl,re,unicodedata
from decimal import Decimal,ROUND_HALF_UP
COUNTRIES={'AUS':'Australia','COL':'Colombia','DEU':'Germany','JPN':'Japan','MEX':'Mexico','TUR':'Türkiye'}
DOMAINS={'SCIE':'Table I.B1.2a.1','READ':'Table I.B1.2a.2','MATH':'Table I.B1.2a.3'}
def normalized(x):return re.sub('[^a-z]','',unicodedata.normalize('NFKD',str(x)).encode('ascii','ignore').decode().lower())
def decimals(fmt):
    # Read the worksheet's publication format; underlying values retain 5 digits.
    fmt=fmt.split(';')[0].replace('"','')
    match=re.search(r'0\.([0#]+)',fmt)
    return len(match.group(1)) if match else 0
def rounded(x,d):return str(Decimal(str(float(x))).quantize(Decimal(10)**-d,rounding=ROUND_HALF_UP))
def main():
    reference=pd.read_csv(ROOT/'data/documentation/official_fay_reference.csv')
    official={(row.pop('country'),row.pop('domain')):row for row in reference.to_dict('records')}
    assert len(official)==18,official.keys()
    cols=['CNT','W_FSTUWT']+[f'W_FSTURWT{r}' for r in range(1,81)]+[f'PV{m}{d}' for d in DOMAINS for m in range(1,11)]
    data=pd.read_parquet(ROOT/'data/processed/pisa2025_ai_subset.parquet',columns=cols)
    meta=load_json('data/processed/stu_metadata.json');rows=[];detail=[]
    for country in COUNTRIES:
        g=data.loc[data.CNT.eq(country)]
        W=g[['W_FSTUWT']+[f'W_FSTURWT{r}' for r in range(1,81)]].to_numpy()
        assert np.isfinite(W).all() and (W>=0).all()
        for d in DOMAINS:
            Y=g[[f'PV{m}{d}' for m in range(1,11)]].to_numpy().copy()
            for m in range(1,11):
                for r in meta['missing_ranges'].get(f'PV{m}{d}',[]):Y[(Y[:,m-1]>=r['lo'])&(Y[:,m-1]<=r['hi']),m-1]=np.nan
            ok=np.isfinite(Y)
            theta=W.T@np.nan_to_num(Y)/(W.T@ok.astype(float))
            Q=theta[0];U=((theta[1:]-Q)**2).sum(axis=0)/20
            u=float(U.mean());b=float(Q.var(ddof=1));mu=float(Q.mean());se=float(np.sqrt(u+1.1*b))
            source=official[(country,d)]
            row={'country':country,'domain':d,'N_total':len(g),'N_PV_valid_min':int(ok.sum(axis=0).min()),'weighted_N':float(W[:,0].sum()),
                 'computed_mean':mu,'computed_SE':se,'sampling_variance_mean':u,'between_PV_variance':b,'total_variance':u+1.1*b,
                 'k':.5,'replicates':80,'plausible_values':10,**source,'source_url':'https://stat.link/mrq53f'}
            for key in ['mean','SE']:
                row[f'{key}_difference']=row[f'computed_{key}']-row[f'official_{key}']
                digits=source[f'{key}_display_decimals']
                row[f'{key}_official_display']=rounded(source[f'official_{key}'],digits)
                row[f'{key}_computed_display']=rounded(row[f'computed_{key}'],digits)
                row[f'{key}_pass']=row[f'{key}_official_display']==row[f'{key}_computed_display']
            row['PASS']=row['mean_pass'] and row['SE_pass'];rows.append(row)
            for m in range(10):detail.append({'country':country,'domain':d,'PV':m+1,'mean':Q[m],'sampling_variance':U[m]})
    result=pd.DataFrame(rows)
    result.to_csv(ROOT/'results/fay2025_validation.csv',index=False,encoding='utf-8-sig')
    pd.DataFrame(detail).to_csv(ROOT/'results/fay2025_validation_by_pv.csv',index=False,encoding='utf-8-sig')
    passed=bool(result.PASS.all())
    message='FAY VALIDATION PASS — k=0.5 empirically reproduces published PISA 2025 SEs' if passed else 'STOP: FAY VALIDATION FAILED'
    status={'status':'PASS' if passed else 'STOP','message':message,'checks':len(result),'passed':int(result.PASS.sum()),
        'criterion':'same display rounding as official workbook cells, before any regression','max_abs_mean_diff':result.mean_difference.abs().max(),
        'max_abs_SE_diff':result.SE_difference.abs().max(),'k':.5,'R':80,'M':10,'source':'OECD I.B1.2a.1–3, StatLink mrq53f'}
    save_json('results/fay2025_validation_status.json',status)
    state=load_json('results/stage2b_status.json');state.update({'status':'PASS WITH RESTRICTED ESTIMAND' if passed else 'STOP','Fay_validation':message})
    save_json('results/stage2b_status.json',state)
    log('Validación empírica de medias y SE 2025',str(status),'Continuar M0/M1/M2 automáticamente' if passed else 'STOP y diagnosticar, sin regresiones')
    print(message,flush=True)
    print(result[['country','domain','computed_mean','official_mean','computed_SE','official_SE','mean_display_decimals','SE_display_decimals','PASS']].to_string(index=False),flush=True)
    if not passed:raise SystemExit(2)

if __name__=='__main__':main()
