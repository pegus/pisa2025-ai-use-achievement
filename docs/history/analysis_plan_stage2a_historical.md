> Historical stage document. The current primary model is CORE (32 countries); see ../../README.md.

> Actualización ETAPA 2B: el usuario aprobó 2A y el estimando restringido. Estado vigente: PASS WITH RESTRICTED ESTIMAND, condicionado únicamente a validar empíricamente medias/SE oficiales 2025 con k=0.5. El STOP de 2A abajo es histórico y queda superado por esta autorización. M0/M1/M2 se ejecutarán solo tras PASS; M3/M4/M5/LDW no se ejecutarán.

# Plan de análisis: uso de IA y rendimiento en PISA 2025

Fecha: 6 de octubre de 2026, America/Bogota. Versión 2, revisada tras la ETAPA 2A y antes de estimar asociaciones entre IA y rendimiento. Estado: **STOP**; ver results/selection_audit.md. M1–M5 no ejecutados.

## Pregunta y alcance de la medición

Evaluar asociaciones, sin asumir la hipótesis ni establecer causalidad. Las cuatro preguntas ST438 registran frecuencia y finalidad declarada, **no prueban sustitución efectiva de procesos cognitivos**. Resumir, investigar y redactar son candidatos conceptuales; investigar puede ser una ayuda legítima. No llamar a sus coeficientes efectos causales del reemplazo cognitivo.

ST436Q16DA registra frecuencia de tareas escolares para evaluar información generada por IA. Es un indicador de oportunidades/prácticas declaradas, no una prueba objetiva de alfabetización ni una intervención asignada al azar. ST436Q02DA permite contrastar con evaluación de información en línea. Interés por aprender IA (IC182Q05DA) no equivale a competencia crítica. PA205Q13DA mide capacidad declarada por **padres**, no por estudiantes; excluirlo de la medida estudiantil.

## Universo y comparabilidad

Estimando principal reformulado: asociación descriptiva dentro de país en la población escolar PISA elegible ex ante para ST438. No generalizar a todos los jóvenes de 15 años. La auditoría documenta ausencias PBA/UH, no cobertura sistemática estadounidense y protocolos pendientes de formas UO en Israel. El indicador observable de administración del archivo de auditoría es un candidato, no certifica la elegibilidad ex ante. Si el dominio no se identifica, limitar explícitamente la descripción a respondientes observados. Antes de modelar, comprobar cobertura conjunta de cada especificación y mostrar todos los flags coverage_75_pass por país y variable, sin exclusiones silenciosas.

Conservar todas las filas del PUF en el reducido. Clasificar miembros con OECD=1, comprobar su coherencia por país y contrastar el conjunto con la documentación oficial del ciclo. CNT identifica países/economías; no confundir SUBNATIO con sistemas independientes. Documentar advertencias de muestreo/adjudicación y modalidades ADMINMODE antes de fijar la lista principal. No excluir un país porque su asociación contradiga la hipótesis.

Construir una tabla de elegibilidad por conducta, país, dominio y especificación. La mera presencia de respuestas válidas no demuestra administración universal o comparabilidad. Auditar códigos 95–99 en ST438, 5–9 en ST436Q16DA, sus rangos SPSS y diferencias por BOOKID/modalidad/país. BOOKID es formulario **de evaluación**; no asumir que es un formulario rotado del cuestionario. Las preguntas IA aparecen en el cuestionario básico CBA; comprobar además PBA y Une Heure y el borrador técnico. Una ausencia estructural se separará de una omisión individual. No ajustar por selección mediante probabilidades inventadas.

## Variables confirmadas

- IA: ST438Q01DA resumir, ST438Q02DA investigar preliminarmente, ST438Q03DA redactar, ST438Q04DA aprender; AIUSESCH índice oficial WLE.
- Categorías originales ST438: 1 nunca/casi nunca; 2 una/dos veces al año; 3 una/dos veces al mes; 4 una/dos veces por semana; 5 diario/casi diario. Referencia=1. Mantener categorías en modelos principales.
- Práctica crítica: ST436Q16DA, 1 nunca/casi nunca, 2 a veces, 3 a menudo, 4 muy a menudo. Comparador general ST436Q02DA.
- Rendimiento: PV1–PV10READ, PV1–PV10MATH, PV1–PV10SCIE. Estimar estadísticas separadas con cada PV, nunca usar su promedio individual como resultado observado.
- Diseño: W_FSTUWT; W_FSTURWT1–80, etiquetados BRR-FAY en PUF y codebook. SENWT verificado: 5000 × W_FSTUWT / suma nacional W_FSTUWT, con suma 5000 por país. **Pendiente verificar el parámetro Fay del ciclo 2025 en documentación específica; no adoptarlo por costumbre.**
- Llaves: CNT+CNTSCHID para escuela y CNT+CNTSTUID para estudiante. Verificar unicidad, cardinalidad y coincidencias antes de cualquier unión. Mantener identificadores como cadenas.

## Covariables y modelos progresivos

M0: N observado, suma de pesos, distribución por frecuencia y medias por dominio, país y promedio de países elegibles. Distinguir tamaño de población ponderado de tamaño efectivo.

Estimar principalmente M1–M5 **por separado dentro de cada país elegible**, con la misma definición de variables y contrastes. M1: categorías IA. M2: añadir ESCS, ST004D01T (sexo/género binario **del marco muestral**, no autodescripción completa), AGE, IMMIG y ST022Q01TA (idioma habitual de casa igual/distinto al del examen). Estos pueden relacionarse con acceso/uso IA y rendimiento. Evaluar disponibilidad antes de exigir casos completos. No sustituir silenciosamente el género del muestreo por el ítem ST430 del cuestionario maestro: ST430Q01DA no aparece en el PUF/codebook local. Los efectos fijos de país corresponden a la sensibilidad multinacional, no a los modelos nacionales principales.

M3: añadir acceso digital doméstico ST250Q02JA y ST250Q05JA, uso general de recursos ST326Q01JA/02JA/04JA/05JA y distracción en ciencias ST097Q06DA. Tratar categorías mediante indicadores. ICTRES/ICTQUAL son alternativas si su cobertura es comparable; evitar incorporar el cuestionario opcional ICT como requisito universal. ESCS ya contiene recursos, y tiempo digital puede incluir IA o actuar como mediador: M3 estima una asociación condicional distinta, no automáticamente una corrección mejor. Informar colinealidad y cambio de muestra.

M4: incorporar composición socioeconómica escolar (media ESCS con ponderación, calculada por escuela y por réplica), tipo/localización escolar y escasez de recursos/personal cuando se verifiquen en SCH. SCH ya fue suministrado. No sustituir datos faltantes por valores de otra escuela. Describir no coincidencias de unión. Inferencia a nivel estudiante con pesos del estudiante; no aplicar el peso escolar como si fuera peso estudiantil.

M5: interacción completa categorías IA × categorías ST436Q16DA, incluyendo efectos principales y controles. Las celdas escasas requieren diagnóstico de soporte; no colapsarlas después de mirar significancias. Contrastar diferencias con covarianza completa. Este análisis no identifica el efecto causal de enseñar alfabetización.

Presentar M2 como especificación principal, M1–M5 como progresión interpretada con cautela. Repetir M1–M3 en muestra común para distinguir ajuste y pérdida de participantes. No imputar datos arbitrariamente. Informar N, pesos y países por cada resultado.

## Estimación y varianza

Con cada PV m, estimar Q_m bajo el peso final y Q_mr bajo cada réplica r. Una vez confirmado el parámetro k y R, usar U_m = [R(1-k)^2]^-1 Σ_r(Q_mr−Q_m)^2; conservar también matrices de covarianza. Combinar Q=promedio_m Q_m, U=promedio_m U_m y B=Σ_m(Q_m−Q)^2/(M−1), T=U+(1+1/M)B. SE=√T. La fórmula y parámetros deben quedar respaldados por documentos oficiales y contrastados con cifras publicadas antes de ejecutar inferencia. IC y pruebas siguen convenciones verificadas OCDE; documentar normalidad/asintótica o grados de libertad aplicados. No usar errores OLS convencionales.

Estrategia principal multinacional: media aritmética de los **coeficientes nacionales** elegibles, dando igual peso a cada país; varianza de diseños nacionales independientes = suma de varianzas/K². Declarar países y K; no llamar OCDE-38 a una media de menos países. No interpretar pesos poblacionales sumados como promedio OCDE. El modelo agrupado con SENWT será **solo sensibilidad**, con normalización a igual suma por país en la muestra de estimación declarada y revisión de esa normalización por réplica. Los índices de réplica de países independientes no se deben perturbar simultáneamente como si representaran un único diseño común: construir contribuciones por país manteniendo los otros países en sus pesos finales, sumar la varianza entre contribuciones y combinar PV. Un coeficiente común agrupado y una media igualitaria de coeficientes nacionales no son el mismo estimando. Mostrar ponderación poblacional como otra sensibilidad.

## Contrastes e hipótesis predefinidas

Analizar las cuatro conductas y los tres dominios. Familia principal: 48 diferencias de las cuatro categorías frente a nunca (4 conductas × 3 dominios × 4 categorías) en M2 y 12 contrastes diario frente a semanal (4×3), total 60. Aplicar BH-FDR a esta familia conjunta; publicar también p sin corregir. H1/H2 se contestan con las diferencias en lectura de resumir/redactar, sin seleccionar frecuencias favorables. H3 diario−semanal conserva covarianza. H4 comparar el patrón de aprender con el de producir textos mediante modelos conjuntos y contrastes de parámetros, no comparando significancia de modelos aislados. H5 prueba conjunta categórica y contrastes predefinidos semanal vs nunca y diario vs semanal; una curva visual no prueba una U.

Moderación H6: interacción categórica, prueba conjunta por conducta/dominio (12 pruebas, familia separada BH). H7 comparar modelos y muestras comunes. H8 efectos fijos y asociaciones nacionales. H9 heterogeneidad de contrastes nacionales. Modelos adicionales, coeficientes por país, índices, splines y términos cuadráticos son secundarios, con familias FDR separadas declaradas. No usar un p<.05 aislado para confirmar la hipótesis global.

Siempre reportar β, SE, IC95%, p y q, puntos PISA, N y países. Para tamaños estandarizados usar SD ponderada del dominio (estimada por PV y réplica cuando afecte inferencia). No convertir puntos PISA en años de aprendizaje mediante una constante universal.

## Índice potencialmente sustitutivo

Estudiar primero correlaciones ordinales ponderadas dentro de país, consistencia y estructura factorial de ST438Q01/02/03. No tratar categorías de frecuencia como intervalos iguales por defecto. Una escala de tres ítems puede tener un modelo unifactorial exactamente identificado, de modo que un ajuste perfecto no valida su estructura. Evaluar invariancia entre países, cargas, consistencia conceptual y sensibilidad por conducta. Una correlación elevada no prueba sustitución cognitiva. Crear SUBSTITUTIVE_AI_INDEX solo con justificación explícita previa a su regresión; si no, mantener ítems separados. No bautizar una suma arbitraria como índice oficial.

## Robustez y heterogeneidad

AIUSESCH continuo y quintiles ponderados si hay soporte/ties manejables, ítems separados, índice candidato si válido, categorías originales, especificación continua/cuadrática secundaria, modelos sin/con controles y muestra común, OECD frente a todos los sistemas elegibles, estimandos senate frente a poblacional, sensibilidad a observaciones influyentes sin recortar PV válidos por intuición y resultados estandarizados por país/PV/réplica. Reportar cambios de signo, precisión y tamaño; no escoger el modelo significativo.

Efectos nacionales por contraste con β, SE, IC, p y N. Meta-análisis solo si el contraste, soporte y medición son comparables; distinguir media igualitaria descriptiva de síntesis por precisión. REML, intervalos apropiados y diagnóstico de heterogeneidad; meta-regresión secundaria limitada por número de países. Presentar forest plots con intervalos y países excluidos con motivo.

## Puertas de calidad y continuación

1. Verificar integridad ZIP y metadatos; cotejar códigos/categorías con codebook y cuestionario.
2. ETAPA 2A terminada: auditar missing, cobertura y diseño de administración, comparabilidad y adjudicación nacional. Resultado STOP; resolver dominio elegible y protocolos pendientes antes de modelos. Ver results/selection_audit.md y los 540 registros país-variable con flags del 75%.
3. Confirmar metodología 2025 (Fay, pesos, PV) con fuente oficial específica. El borrador técnico aún no se ha podido descargar (HTTP 403 y timeout del navegador). La guía OCDE general contiene ejemplos de ciclos antiguos y no basta para confirmar el factor 2025.
4. Reproducir distribuciones del compendio oficial y al menos una media de rendimiento, con sus SE; documentar denominadores y tolerancias de redondeo antes de evaluar. El compendio puede incluir no respuesta dentro de su denominador; no compararlo directamente con porcentajes solo de respuestas sustantivas.
5. Si cualquiera de estos puntos falla de forma material, detener inferencia, registrar el motivo y preservar los archivos. No rellenar tablas ni gráficos con resultados simulados.

Actualización documental posterior a la preparación, aún antes de asociaciones: ST438 y ST436Q16DA aparecen en el cuestionario CBA y no se localizan en los maestros PBA/UH. La población que contesta IA puede excluir sistemáticamente alumnos de bajo desempeño asignados a UH. Esto constituye un impedimento serio para generalización sin comprobar selección, alcance del estimando y tratamiento oficial. No transformar ausencia estructural en “nunca”.

Tras validar: descriptivos → modelos → países → robustez → ocho visualizaciones con IC → artículo científico. Seeds para procedimientos aleatorios=20251006; análisis deterministas sin aleatorización. Versiones en results/package_versions.json. Scripts y manifiestos permiten reanudar sin repetir extracción.

## Segunda fase LDW

LDW es Learning in the Digital World: resolución de problemas y construcción de conocimiento con herramientas computacionales. El código oficial identifica PV1–10CMPS, CPPK, CMOD y CPRO en STU; el archivo LDW contiene respuestas, tiempos y acciones, no un índice genérico de autonomía. No unir archivos ni probar hipótesis LDW antes de fijar su definición y condiciones de administración. Verificar CNT+CNTSTUID, relación 1:1 o cobertura parcial y pérdidas de unión. Las escalas SELFREG de cuestionario también requieren validación conceptual antes de identificarlas con autonomía. Esta fase queda posterior al análisis académico principal.
