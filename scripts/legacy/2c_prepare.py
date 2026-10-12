"""Availability-only decisions: no AI coefficients or outcomes are examined."""
from common import ROOT,load_json,save_json,log
import numpy as np,pandas as pd,pyreadstat,hashlib
AI=[f'ST438Q0{i}DA' for i in range(1,5)]
FULL=['ESCS','ST004D01T','AGE','IMMIG','ST022Q01TA']
CORE=['ESCS','IMMIG','ST022Q01TA']
ACCESS=['ST250Q02JA','ST250Q05JA']
AMBIG=['ST326Q01JA','ST326Q02JA','ST326Q04JA','ST326Q05JA','ST097Q06DA']
EXTRA=['ST127Q01TA','ST127Q02TA','ST127Q03TA','ST062Q01TA','ST062Q02TA','ST062Q03TA','ST001D01T',
       'IC171Q01JA','IC171Q02JA','IC171Q05JA','IC171Q06JA','ST322Q07JA']
def write(df,name):df.to_csv(ROOT/'results'/name,index=False,encoding='utf-8-sig',float_format='%.12g')
def clean(df):
    meta=load_json('data/processed/stu_metadata.json')
    for v in df:
        for r in meta['missing_ranges'].get(v,[]):df.loc[df[v].between(r['lo'],r['hi']),v]=np.nan
    return df
def main():
    raw=ROOT.parent/'work/raw/CY09_MS_STU_PUF.sav'
    extra,meta=pyreadstat.read_sav(str(raw),usecols=['CNT','CNTSTUID']+EXTRA,user_missing=True)
    extra=clean(extra)
    base=pd.read_parquet(ROOT/'data/processed/pisa2025_ai_subset.parquet')
    assert not base[['CNT','CNTSTUID']].duplicated().any()
    assert not extra[['CNT','CNTSTUID']].duplicated().any()
    data=clean(base.merge(extra,on=['CNT','CNTSTUID'],how='left',validate='one_to_one'))
    assert len(data)==755721
    data=data.loc[data.OECD.eq(1)].copy()
    data.to_parquet(ROOT/'data/processed/pisa2025_stage2c_oecd.parquet',index=False)
    eligibility=pd.read_csv(ROOT/'results/stage2b_country_eligibility.csv')
    candidates=sorted(eligibility.loc[eligibility.ST438_all_four_75_pass,'country'])
    full21=sorted(pd.read_csv(ROOT/'results/primary_contrasts_M2.csv').iloc[0].countries.split(';'))
    assert len(candidates)==36 and len(full21)==21
    covrows=[];concept={
      'ESCS':('probable_confounder','family socioeconomic/cultural background; may include current possessions'),
      'IMMIG':('probable_confounder','migration background largely precedes current reported AI use'),
      'ST022Q01TA':('probable_confounder','home language/background plausibly precedes reported AI use'),
      'ST004D01T':('probable_confounder','sampling-frame sex, nationally absent in many countries'),
      'AGE':('probable_confounder','chronological age, narrow range and nationally absent in two systems'),
      'ST250Q02JA':('probable_confounder','home computer availability plausibly enables AI use; temporal order not observed'),
      'ST250Q05JA':('probable_confounder','home internet availability plausibly enables AI use; temporal order not observed'),
      'ST326Q01JA':('ambiguous','current-year digital learning may include AI and may change after AI adoption'),
      'ST326Q02JA':('ambiguous','current-year out-of-school digital learning may include AI and may change after adoption'),
      'ST326Q04JA':('ambiguous','current digital leisure may proxy prior preferences or respond to AI adoption'),
      'ST326Q05JA':('ambiguous','current out-of-school leisure: unverified temporal order; not automatically pre-exposure'),
      'ST097Q06DA':('possible_mediator','current classroom digital distraction may follow use and is science-specific')}
    for c,g in data.loc[data.CNT.isin(candidates)].groupby('CNT'):
        total=g.W_FSTUWT.sum()
        for v in FULL+ACCESS+AMBIG+EXTRA:
            ok=g[v].notna();pct=100*g.loc[ok,'W_FSTUWT'].sum()/total
            cls,why=concept.get(v,('diagnostic_only','primary-school repetition can precede current AI; other repetition/absence timing uncertain' if v.startswith(('ST127','ST062','ST001')) else 'digital comparison, not a validated negative control'))
            covrows.append({'country':c,'candidate':v,'N_total':len(g),'N_valid':int(ok.sum()),'weighted_N_total':total,
                'weighted_N_valid':g.loc[ok,'W_FSTUWT'].sum(),'coverage_pct':pct,'coverage_75_pass':pct>=75,
                'nationally_absent':not ok.any(),'chosen_M2_core':v in CORE,'chosen_M2_full':v in FULL,
                'chosen_M3_confounders':v in ACCESS,'chosen_M3_including_potential_mediators':v in ACCESS+AMBIG,
                'conceptual_class':cls,'reason':why,'selection_uses_AI_coefficients':False})
    av=pd.DataFrame(covrows);write(av,'M2_core_country_availability.csv')
    summary=av.groupby('candidate').agg(countries_75=('coverage_75_pass','sum'),nationally_absent=('nationally_absent','sum'),min_pct=('coverage_pct','min'),median_pct=('coverage_pct','median'))
    write(summary.reset_index(),'stage2c_variable_availability_summary.csv')
    spec={'candidate_countries':candidates,'full21':full21,'M2_CORE':CORE,'M2_FULL':FULL,'M3_CONFOUNDERS':ACCESS,
       'M3_AMBIGUOUS_POTENTIAL_MEDIATORS':AMBIG,'digital_comparison_exposures':['IC171Q01JA','IC171Q05JA','IC171Q06JA','ST322Q07JA'],
       'CORE_decision':'Keep three prioritized background confounders; do not make sex or age mandatory. Maximization subject to conceptual adequacy, not ESCS-only deletion of migration/home language.',
       'decision_basis':'Availability and official item wording only; no new AI coefficients examined before this file.',
       'primary_joint_coverage_threshold':75,'school_support':{'minimum_informative_schools':30,'minimum_N_per_category':30,'max_gram_condition':1e12},
       'joint_support':{'minimum_N_per_category':30,'minimum_effective_N_per_category':10,'max_VIF_ai_dummy':10,'max_standardized_design_condition':30},
       'comparison_intensive_group_IC':'categories 4/5 daily; reference 1 never; category 6 unavailable retained as separate nuisance category',
       'cross_domain_inference':'Common sample and matching replicate weights. Paired-PV covariance provided as sensitivity until joint PV draw alignment is documented; primary inference uses maximum sampling variance across feasible PV pairings plus conservative between-PV covariance bound.',
       'H15_comparable_rule':'paired beta change within +/-5 PISA points by 90% CI (equivalence); sign alone insufficient',
       'FDR':'BH60 separately for each model/base; BH16 specificity per model; BH9 learn pattern per model/base; all stage2c tests secondary/exploratory',
       'no_LDW_no_final_article':True}
    save_json('results/stage2c_specification.json',spec)
    protocol='''# ETAPA 2C: decisiones fijadas antes de los nuevos coeficientes

Aceptación 2B: mantener estimando restringido, 10 PV, 80 réplicas y Fay k=.5 validado empíricamente. No LDW, artículo ni conclusión causal.

M2-CORE = ESCS + IMMIG categórico + lengua del hogar. Se priorizan las tres variables solicitadas, se rechaza elegir por significancia o signo. La edad tiene rango estrecho y pérdidas nacionales; sexo impide comparabilidad amplia. No se elimina migración/lengua solo para rescatar un país adicional con ausencia completa. M2-FULL conserva exactamente los cinco controles 2B.

M2-SCHOOL-FE se estima con base CORE y también FULL. País/escuela = CNT+CNTSCHID. Se exige al menos 30 escuelas con >1 categoría observada y 30 estudiantes por categoría, rango identificable y condición Gram <1e12 en TODAS las réplicas. Las escuelas sin variación no identifican directamente el contraste; se conservan y describen, pueden informar covariables. Se recalculan productos y medias ponderadas por escuela con cada réplica. Las diez respuestas PV usan sus propias medias ponderadas; solo X y pesos, que no dependen del PV, se comparten por eficiencia.

M3-CONFOUNDERS añade computadora e internet domésticos a CORE (y FULL secundario). M3-INCLUDING-POTENTIAL-MEDIATORS añade además los cuatro tiempos de uso digital ya predefinidos y distracción digital. Los tiempos actuales son ambiguos, la distracción puede mediar: no se los transforma en confusores preexistentes por conveniencia. Se codifican por indicadores, sin imponer intervalos iguales.

Modelo conjunto: cuatro exposiciones categóricas simultáneas + CORE, FULL secundario. Soporte: >=30 por categoría y n efectivo Kish >=10, todas las réplicas con rango completo; VIF máximo de indicadores IA <=10 y condición del diseño estandarizado <=30. Si falla, conservar diagnóstico/estimación exploratoria y excluir síntesis interpretable. Tabular 625 perfiles y 6 tablas bivariadas de 25 celdas por país, sin seleccionar por resultados.

A–E: resúmenes originales por países solicitados. Descomponer adicionalmente con M1 reestimado sobre exactamente los casos completos de CORE/FULL y ambos modelos sobre la misma muestra: separar cambio de países, selección de estudiantes y cambio de especificación. No llamar causal a la diferencia al ajustar. Contrastes de cambios usan mismas réplicas/PV.

Especificidad: probar READ-MATH y READ-SCIE directamente para diario-nunca y diario-semanal, usando misma muestra. Covarianza muestral identificable por mismas 80 réplicas. No certificar alineación conjunta de sorteos PV entre dominios por solo coincidir números. Publicar inferencia conservadora: U_diferencia + 1.1*(sqrt(B_READ)+sqrt(B_otro))²; emparejamiento PV por número como sensibilidad. BH16 por modelo. También magnitudes en SD nacional como sensibilidad descriptiva a escalas.

Repetición primaria ST127Q01TA: antecedente más defendible; no prueba fecha anterior a cualquier IA. Repetición otros niveles y ausentismo en últimas dos semanas: diagnósticos temporales ambiguos. No ajustar rendimiento PISA, autoeficacia o motivación actuales. Comparaciones digitales IC171 computador/software/juegos y ST322 ansiedad: comportamientos o recursos no específicamente IA, pueden solaparse con IA; se llaman comparison controls, nunca negative controls validados. No usar IC170/171Q10 (IA) como control negativo.

Hipótesis H10–H15 secundarias, resultados supported/mixed/not supported. Para H15 equivalencia +/-5 puntos con IC90 de diferencias emparejadas; no declarar comparable por falta de significancia. Heterogeneidad I², rango, signos, REML-HK y forest; correlaciones ecológicas exploratorias con penetración IA, rendimiento/ESCS nacional y cobertura, sin interpretación individual/causal.
'''
    # Preserve the dated historical plan including supplemental classification rules.
    # Runtime protocol is saved separately; statistical specification is unchanged.
    (ROOT/'STAGE_2C_RUNTIME_PLAN.md').write_text(protocol,encoding='utf-8')
    print(summary.to_string(),flush=True)
    log('Preespecificación 2C y disponibilidad','CORE/FE/M3/conjunto/diagnósticos definidos antes de nuevos coeficientes','Separar muestra, países y controles; conservar no estimables')
if __name__=='__main__':main()
