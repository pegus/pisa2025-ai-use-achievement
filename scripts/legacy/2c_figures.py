import os
from common import ROOT
os.environ['MPLCONFIGDIR']=str(ROOT.parent/'work/matplotlib_config')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd,numpy as np
AI=[f'ST438Q0{i}DA' for i in range(1,5)];LABEL=['Resumir','Investigar','Redactar','Ayudar a aprender']
plt.rcParams.update({'font.size':12,'axes.titlesize':15,'axes.labelsize':12,'xtick.labelsize':11,'ytick.labelsize':11,'legend.fontsize':11})
F=ROOT/'figures';F.mkdir(exist_ok=True)
def finish(fig,name,footer):
    fig.get_layout_engine().set(rect=(0,.07,1,.93))
    fig.text(.04,.02,footer,fontsize=11,ha='left');fig.savefig(F/name,dpi=165,bbox_inches='tight');plt.close(fig)
def main():
    national=pd.read_csv(ROOT/'results/stage2c_all_national_models.csv');summary=pd.read_csv(ROOT/'results/stage2c_equal_weight_summary.csv')
    changes=pd.read_csv(ROOT/'results/stage2c_paired_model_changes.csv');progress=pd.read_csv(ROOT/'results/model_progression_same_sample.csv')
    domain=pd.read_csv(ROOT/'results/domain_specificity_tests.csv')
    fig,axes=plt.subplots(2,2,figsize=(14,11),layout='constrained')
    for exp,label,ax in zip(AI,LABEL,axes.ravel()):
        for base,color,marker in [('CORE','#1769aa','o'),('FULL','#bb4e16','s')]:
            new=national.loc[national.model.eq('M2-SCHOOL-FE')&national.base_controls.eq(base)&national.exposure.eq(exp)&national.domain.eq('READ')&national.contrast.eq('daily_vs_never')&national.primary_synthesis_eligible]
            old=national.loc[national.model.eq('M2-NO-FE-SAME-SAMPLE')&national.base_controls.eq(base)&national.exposure.eq(exp)&national.domain.eq('READ')&national.contrast.eq('daily_vs_never')]
            g=new.merge(old,on='country',suffixes=('_FE','_sinFE'));ax.scatter(g.beta_sinFE,g.beta_FE,s=35,c=color,marker=marker,alpha=.65,label=f'{base}, K={len(g)}')
            ax.scatter(g.beta_sinFE.mean(),g.beta_FE.mean(),s=150,c=color,marker='X',edgecolors='black')
            row=changes.loc[changes.new_model.eq('M2-SCHOOL-FE')&changes.base_controls.eq(base)&changes.exposure.eq(exp)&changes.domain.eq('READ')&changes.contrast.eq('daily_vs_never')].iloc[0]
            ax.text(.03,.06 if base=='CORE' else .12,f'{base}: cambio medio {row.delta_beta:+.1f} puntos',transform=ax.transAxes,color=color,fontsize=11)
        limits=[min(ax.get_xlim()[0],ax.get_ylim()[0]),max(ax.get_xlim()[1],ax.get_ylim()[1])];ax.plot(limits,limits,'--',c='gray',lw=1);ax.axhline(0,c='gray',lw=.8);ax.axvline(0,c='gray',lw=.8)
        ax.set(xlabel='Sin efectos fijos (misma muestra)',ylabel='Con efectos fijos de escuela',title=label+' · diario frente a nunca');ax.legend(loc='upper left');ax.grid(alpha=.15)
    fig.suptitle('Lectura: asociaciones dentro de la misma escuela',fontsize=20)
    finish(fig,'school_FE_comparison.png','Cada punto es un país; X = media igualitaria. Controles y estudiantes constantes. Asociaciones, sin interpretación causal.')
    fig,axes=plt.subplots(2,2,figsize=(14,11),layout='constrained');stages=['A_M1_36','B_M1_21','C_M2_CORE_all_eligible','D_M2_CORE_21','E_M2_FULL_21']
    for exp,label,ax in zip(AI,LABEL,axes.ravel()):
        r=progress.loc[progress.exposure.eq(exp)&progress.domain.eq('READ')&progress.contrast.eq('daily_vs_never')].iloc[0]
        b=[r[t+'_beta'] for t in stages];se=[r[t+'_SE'] for t in stages]
        ax.errorbar(np.arange(5),b,yerr=1.959964*np.array(se),marker='o',c='#1769aa',capsize=4)
        ax.set_xticks(range(5),[f'{l}\nK={int(r[t+"_K"])}' for l,t in zip(['M1 todos','M1 21','CORE todos','CORE 21','FULL 21'],stages)])
        ax.axhline(0,c='gray',lw=1);ax.grid(axis='y',alpha=.2);ax.set(title=label+' · diario frente a nunca',ylabel='Asociación con lectura (puntos)')
        ax.text(.02,.03,f'A→C: países {r.A_to_C_country_component:+.1f}; estudiantes {r.A_to_C_student_selection_component:+.1f}; controles {r.A_to_C_controls_same_students_component:+.1f}',transform=ax.transAxes,fontsize=10)
    fig.suptitle('Progresión del modelo: separar ajuste y composición',fontsize=20)
    finish(fig,'model_progression.png','IC95 BRR-Fay y 10 PV. Los tramos cambian países y/o muestras; la tabla CSV contiene la descomposición emparejada.')
    fig,axes=plt.subplots(2,2,figsize=(15,11),layout='constrained');specs=[('M2-CORE','CORE','CORE'),('M2-FULL','FULL','FULL'),('M2-SCHOOL-FE','CORE','FE'),('M3-CONFOUNDERS','CORE','M3 acceso'),('JOINT-AI-USES','CORE','Conjunto')]
    colors=['#1769aa','#bb4e16','#209d77','#7f55ac','#555555']
    for exp,label,ax in zip(AI,LABEL,axes.ravel()):
        for k,((model,base,short),color) in enumerate(zip(specs,colors)):
            g=domain.loc[domain.model.eq(model)&domain.base_controls.eq(base)&domain.exposure.eq(exp)]
            for j,(contrast,diff) in enumerate([('daily_vs_never','READ_minus_MATH'),('daily_vs_never','READ_minus_SCIE'),('daily_vs_weekly','READ_minus_MATH'),('daily_vs_weekly','READ_minus_SCIE')]):
                r=g.loc[g.contrast.eq(contrast)&g.difference.eq(diff)].iloc[0]
                ax.errorbar(r.beta,j+(k-2)*.13,xerr=1.959964*r.SE,fmt='o',color=color,capsize=2,label=short if j==0 else None)
        ax.set_yticks(range(4),['Diario–nunca\nREAD−MATH','Diario–nunca\nREAD−SCIE','Diario–semanal\nREAD−MATH','Diario–semanal\nREAD−SCIE']);ax.invert_yaxis();ax.axvline(0,c='gray',lw=1)
        ax.set(title=label,xlabel='Diferencia directa de coeficientes (puntos)');ax.grid(axis='x',alpha=.2);ax.legend(loc='lower right' if exp==AI[3] else 'lower left',ncol=2)
    fig.suptitle('Especificidad por dominio: valores negativos favorecen una asociación más negativa en lectura',fontsize=17)
    finish(fig,'domain_specificity.png','IC95 conservadores: covarianza BRR y cota de incertidumbre PV. CSV incluye comparación emparejada por PV y magnitudes en SD.')
    def forest(model,base,d,contrast):
        fig,axes=plt.subplots(1,4,figsize=(17,17),sharex=True,layout='constrained')
        for exp,label,ax in zip(AI,LABEL,axes):
            g=national.loc[national.model.eq(model)&national.base_controls.eq(base)&national.exposure.eq(exp)&national.domain.eq(d)&national.contrast.eq(contrast)&national.primary_synthesis_eligible].sort_values('country')
            countries=g.country.tolist();y=np.arange(len(g))
            ax.errorbar(g.beta,y,xerr=1.959964*g.SE,fmt='o',ms=4,c='#1769aa',capsize=2)
            r=summary.loc[summary.model.eq(model)&summary.base_controls.eq(base)&summary.exposure.eq(exp)&summary.domain.eq(d)&summary.contrast.eq(contrast)].iloc[0]
            ax.errorbar(r.beta,len(g)+1,xerr=1.959964*r.SE,fmt='D',c='#bb4e16',capsize=4,ms=7)
            ax.set_yticks(list(y)+[len(g)+1],countries+['Media igual']);ax.invert_yaxis();ax.axvline(0,c='gray',lw=1);ax.set(title=f'{label}\nK={int(r.K)} · I²={r.I2_pct:.1f}%',xlabel='Coeficiente (puntos)');ax.grid(axis='x',alpha=.2)
        fig.suptitle(f'{model} · {base} · {d} · {contrast}',fontsize=20)
        fig.get_layout_engine().set(rect=(0,.05,1,.95))
        fig.text(.03,.02,'IC95 BRR-Fay y 10 PV; países con cobertura conjunta ≥75% y soporte. La media representa el conjunto fijo; sin causalidad.',fontsize=11)
        return fig
    fig=forest('M2-SCHOOL-FE','CORE','READ','daily_vs_never');fig.savefig(F/'updated_forest_plots.png',dpi=155,bbox_inches='tight');plt.close(fig)
    # Complete central forests for all models and domains, readable full pages.
    with PdfPages(F/'updated_forest_plots_all_models.pdf') as pdf:
        for model,base in [('M2-CORE','CORE'),('M2-FULL','FULL'),('M2-SCHOOL-FE','CORE'),('M2-SCHOOL-FE','FULL'),('M3-CONFOUNDERS','CORE'),('M3-CONFOUNDERS','FULL'),('M3-INCLUDING-POTENTIAL-MEDIATORS','CORE'),('M3-INCLUDING-POTENTIAL-MEDIATORS','FULL'),('JOINT-AI-USES','CORE'),('JOINT-AI-USES','FULL')]:
            for d in ['READ','MATH','SCIE']:
                for contrast in ['daily_vs_never','daily_vs_weekly']:
                    fig=forest(model,base,d,contrast);pdf.savefig(fig,bbox_inches='tight');plt.close(fig)
    print('Four requested PNGs and complete forest PDF written',flush=True)
if __name__=='__main__':main()
