from common import ROOT,load_json
import pandas as pd,numpy as np
from importlib.util import spec_from_file_location,module_from_spec
sp=spec_from_file_location('s',ROOT/'scripts/2b_synthesize.py');s=module_from_spec(sp);sp.loader.exec_module(s)
sp=spec_from_file_location('m',ROOT/'scripts/2c_models.py');m=module_from_spec(sp);sp.loader.exec_module(m)
def main():
    a=pd.read_csv(ROOT/'results/digital_comparison_same_sample.csv');b=pd.read_csv(ROOT/'results/digital_task_comparison_results.csv');df=pd.concat([a,b],ignore_index=True)
    rows=[];reml=[]
    for (digital,exposure,domain,contrast),g in df.groupby(['digital_comparator','exposure','domain','contrast']):
        if domain=='ALL' or contrast=='not_estimable':continue
        g=g.loc[g.primary_synthesis_eligible&g.fit_status.eq('estimated')]
        info={'digital_comparator':digital,'exposure':exposure,'domain':domain,'contrast':contrast,'same_students_for_AI_and_digital':True}
        rows.append({**info,**s.summarize(g)});reml.append({**info,**s.reml(g)})
    summary=pd.DataFrame(rows);summary['q_FDR_comparison']=summary.groupby('digital_comparator').p_raw.transform(s.bh)
    m.write(summary,'digital_comparison_same_sample_summary.csv');m.write(pd.DataFrame(reml),'digital_comparison_REML.csv')
    print('Digital comparison summaries complete',flush=True)
if __name__=='__main__':main()
