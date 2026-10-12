from common import ROOT,load_json
import pandas as pd,numpy as np,itertools
from importlib.util import spec_from_file_location,module_from_spec
sp=spec_from_file_location('m',ROOT/'scripts/2c_models.py');m=module_from_spec(sp);sp.loader.exec_module(m)
def main():
    data=pd.read_parquet(ROOT/'data/processed/pisa2025_stage2c_oecd.parquet');spec=load_json('results/stage2c_specification.json');profiles=[];pairs=[]
    for c in spec['candidate_countries']:
        g=data.loc[data.CNT.eq(c)]
        for base,controls in [('CORE',m.CORE),('FULL',m.FULL)]:
            if base=='FULL' and c not in spec['full21']:continue
            sub=g.loc[m.make_mask(g,m.AI,controls)];a=sub[m.AI].to_numpy(int);w=sub.W_FSTUWT.to_numpy()
            index=((a-1)*np.array([125,25,5,1])).sum(axis=1);counts=np.bincount(index,minlength=625);weights=np.bincount(index,weights=w,minlength=625)
            for j,cats in enumerate(itertools.product(range(1,6),repeat=4)):
                profiles.append({'country':c,'base_controls':base,**dict(zip(m.AI,cats)),'N':counts[j],'weighted_N':weights[j],
                    'zero_profile':counts[j]==0,'N_lt_10':counts[j]<10,'sample':'exact JOINT-AI-USES analytical complete cases'})
            for i,j in itertools.combinations(range(4),2):
                index=(a[:,i]-1)*5+a[:,j]-1;counts=np.bincount(index,minlength=25);weights=np.bincount(index,weights=w,minlength=25)
                for k,cats in enumerate(itertools.product(range(1,6),repeat=2)):
                    pairs.append({'country':c,'base_controls':base,'exposure_A':m.AI[i],'exposure_B':m.AI[j],'category_A':cats[0],
                         'category_B':cats[1],'N':counts[k],'weighted_N':weights[k],'zero_cell':counts[k]==0,'N_lt_10':counts[k]<10,
                         'sample':'exact JOINT-AI-USES analytical complete cases'})
    m.write(pd.DataFrame(profiles),'joint_AI_analytical_profile_support.csv');m.write(pd.DataFrame(pairs),'joint_AI_analytical_pairwise_cells.csv')
    print('Joint analytical cell support complete',flush=True)
if __name__=='__main__':main()
