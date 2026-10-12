from common import ROOT,load_json,log
import os
config=ROOT.parent/'work/matplotlib_config';config.mkdir(exist_ok=True)
os.environ['MPLCONFIGDIR']=str(config)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
NAMES={'ST438Q01DA':'Resumir textos','ST438Q02DA':'Investigación preliminar','ST438Q03DA':'Redactar trabajos','ST438Q04DA':'Ayudar a aprender'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'axes.titlesize':15,'axes.labelsize':12,'xtick.labelsize':11,'ytick.labelsize':11,
                     'savefig.facecolor':'white','axes.spines.top':False,'axes.spines.right':False})
def main():
    country=pd.read_csv(ROOT/'results/country_effects_M2.csv');summary=pd.read_csv(ROOT/'results/primary_contrasts_M2.csv')
    path=ROOT/'figures';path.mkdir(exist_ok=True)
    g=country.loc[country.domain.eq('READ')&country.contrast.eq('daily_vs_never')&country.fit_status.eq('estimated')&country.primary_synthesis_eligible]
    countries=sorted(g.country.unique());labels=['Media igualitaria']+countries;y=np.arange(len(labels))
    fig,axes=plt.subplots(1,4,figsize=(19,12),sharey=True)
    xmin=min(g.CI_low.min(),summary.loc[summary.domain.eq('READ'),'CI95_low'].min())-4
    xmax=max(g.CI_high.max(),5)+4
    for ax,(exposure,label) in zip(axes,NAMES.items()):
        h=g.loc[g.exposure.eq(exposure)].set_index('country').reindex(countries)
        r=summary.loc[summary.exposure.eq(exposure)&summary.domain.eq('READ')&summary.contrast.eq('daily_vs_never')].iloc[0]
        b=h.beta.to_numpy();err=np.vstack([b-h.CI_low,h.CI_high-b]);ax.errorbar(b,y[1:],xerr=err,fmt='o',color='#24688f',markersize=5,capsize=2,lw=1.2)
        ax.errorbar(r.beta,0,xerr=[[r.beta-r.CI95_low],[r.CI95_high-r.beta]],fmt='D',color='#111111',markersize=7,capsize=4,lw=2)
        ax.axvline(0,color='#777777',linestyle='--',lw=1);ax.axhline(.5,color='#dddddd',lw=1);ax.set_xlim(xmin,xmax)
        ax.set_title(label);ax.set_xlabel('Diferencia en puntos PISA');ax.grid(axis='x',color='#eeeeee');ax.set_yticks(y)
    axes[0].set_yticklabels(labels);axes[0].invert_yaxis()
    fig.suptitle('Lectura: uso diario frente a nunca o casi nunca — M2',fontsize=19,y=.975)
    fig.text(.5,.025,'IC 95% con 10 valores plausibles y 80 réplicas BRR-Fay (k=0,5). Países con cobertura conjunta ≥75%.\nM2 ajusta ESCS, sexo, edad, inmigración y lengua del hogar. Asociación descriptiva, sin interpretación causal.',ha='center',fontsize=12)
    fig.subplots_adjust(left=.12,right=.985,top=.91,bottom=.10,wspace=.12)
    fig.savefig(path/'forest_reading_summary.png',dpi=170);plt.close(fig)
    fig,axes=plt.subplots(2,2,figsize=(14,10),sharex=True,sharey=True)
    contrast=['yearly_vs_never','monthly_vs_never','weekly_vs_never','daily_vs_never']
    for ax,(exposure,label) in zip(axes.flat,NAMES.items()):
        h=summary.loc[summary.exposure.eq(exposure)&summary.domain.eq('READ')].set_index('contrast').reindex(contrast)
        values=np.r_[0,h.beta.to_numpy()];low=np.r_[0,h.CI95_low.to_numpy()];high=np.r_[0,h.CI95_high.to_numpy()]
        ax.plot(range(5),values,'o-',color='#24688f',lw=2)
        ax.errorbar(range(1,5),values[1:],yerr=np.vstack([values[1:]-low[1:],high[1:]-values[1:]]),fmt='none',color='#24688f',capsize=4)
        ax.scatter([0],[0],marker='s',s=40,color='#111111');ax.axhline(0,color='#888888',lw=1,linestyle='--')
        ax.set_title(label+f' (K={int(h.K.iloc[0])})');ax.grid(axis='y',color='#eeeeee')
        ax.set_xticks(range(5),['Nunca','Anual','Mensual','Semanal','Diario']);ax.set_ylabel('Diferencia frente a nunca (puntos)')
    fig.suptitle('Frecuencia declarada de IA y lectura: asociaciones M2',fontsize=19,y=.98)
    fig.text(.5,.025,'Media igualitaria de coeficientes nacionales e IC 95%. Nunca es la referencia fijada en cero, sin un IC propio.\nLos segmentos unen categorías ordinales; no suponen intervalos iguales ni una curva continua. No representa causalidad.',ha='center',fontsize=12)
    fig.subplots_adjust(left=.085,right=.98,top=.91,bottom=.13,hspace=.22,wspace=.12)
    fig.savefig(path/'ai_frequency_reading.png',dpi=180);plt.close(fig)
    log('Figuras de lectura M2','Forest nacional y perfiles categóricos','Mostrar IC del diseño y referencia, sin curvas causales ni PV individuales promediados')

if __name__=='__main__':main()
