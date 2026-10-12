> Historical stage document. The current primary model is CORE (32 countries); see ../../README.md.

> Estado posterior a esta auditoría histórica: ETAPA 2A aprobada por el usuario. ETAPA 2B tiene PASS WITH RESTRICTED ESTIMAND, con validación Fay 18/18 y M0/M1/M2 completados. El STOP de este documento es la decisión original de 2A, no el estado global vigente. Véase STAGE_2B_REPORT.md.

# ETAPA 2A — Auditoría de selección y cobertura de IA, PISA 2025

Fecha: 6 de octubre de 2026. **Conclusión operativa: STOP. M1–M5 no ejecutados.**

El análisis propuesto para «todos los estudiantes de 15 años» no queda respaldado por la cobertura de ST438. La ausencia incluye grupos seleccionados por el diseño y, en Estados Unidos, no cobertura sistemática documentada. Un análisis reformulado de la población elegible podría ser viable, con países y denominadores explícitos, pero aún no se ha confirmado la constante numérica Fay de 2025 ni cerrado la administración de los formularios UO. STOP se refiere al análisis poblacional e inferencial propuesto; no demuestra que toda investigación sobre IA sea imposible ni que exista un efecto causal.

## 1. Base auditada y significado de N

Se conservaron **755,721 estudiantes**, **90 países/economías** y **38 miembros OCDE** según OECD=1 en el PUF. El portal enumera 91 sistemas; QCY (Chipre) aparece en el codebook pero no tiene registros en el archivo suministrado. No se inventó una fila de población ni una cobertura cero para ese sistema: queda **no disponible** fuera de las 90 unidades observadas.

En cada país, N_total es el número de registros, y weighted_N_total=ΣW_FSTUWT es la población escolar PISA representada por esos registros: no es tamaño efectivo ni una cuenta de todos los adolescentes, incluidos quienes están fuera de la población definida o excluidos del estudio. La suma de pesos de los 90 sistemas es 32,824,943.82; no se usa como promedio OCDE. Tampoco se reconstruye aquí la cobertura del marco muestral o las tasas de respuesta de escuelas/alumnos no presentes en el PUF.

`ai_coverage_by_country.csv` contiene **540 filas** (90×6), N y suma de pesos para cada categoría, porcentajes con denominador nacional completo y ADMINMODE. Los códigos originales se conservan en `selection_audit_raw.parquet`; el reducido mantiene null para missing documentados y ahora incluye **SENWT y Option_UH, 156 columnas**. Todas las categorías de missing son mutuamente excluyentes y suman el total; no hay códigos inesperados en estas seis variables.

## 2. SENWT: verificación y relación matemática

El SPSS y el codebook coinciden en la etiqueta **Senate Weight (sum of 5000 per country)**. Para cada estudiante i del país c:

    SENWT_ic = W_FSTUWT_ic × 5000 / Σ_j∈c W_FSTUWT_jc

La fórmula se verificó en todos los registros y la suma nacional es 5000 en los 90 sistemas. Máxima diferencia relativa observada: 4.52e-14. Evidencia completa: `senate_weight_audit.csv`. Es una reescala constante dentro de país: conserva proporciones, medias y coeficientes de un modelo nacional ponderado invariante a esa reescala. No añade corrección por elegibilidad ni convierte en representativa una selección de respondientes.

Al filtrar una muestra, la suma de los SENWT originales deja de ser necesariamente 5000. En una sensibilidad agrupada se deberá decidir y declarar si se conserva la masa elegible o se renormaliza a 5000 dentro de la muestra analítica de cada país; son estimandos distintos. SENWT no trae por sí solo la replicación conjunta de diseños nacionales independientes. Los códigos oficiales usan senwt para dar igual importancia a países en un ejemplo de recodificación; no se ejecutó ese ejemplo como regresión de esta investigación.

## 3. Estándar 6.15 y cobertura válida

El [estándar PISA 2025 6.15, página 30](https://www.oecd.org/content/dam/oecd/en/about/programmes/edu/pisa/publications/technical-standards/PISA_2025_Technical_Standards.pdf) exige señalar o sustituir por missing los análisis de cuestionario que no vinculen al menos el 75% ponderado de la población objetivo. Se aplicó una regla explícita por variable:

    coverage_75_pass = ΣW(respuesta válida al ítem/índice) / ΣW(todos los registros nacionales) ≥ 0.75

Es una aplicación operativa a los respondientes ponderados del PUF, conforme al vínculo con el estándar 6.14; no equivale a certificar la adjudicación nacional ni la cobertura de todos los jóvenes. Para una futura especificación también habrá que comprobar el porcentaje que vincula **todas** las variables usadas, no únicamente cada una por separado. El archivo `selection_candidate_domains.csv` muestra, entre otros, el cruce cuatro ST438 válidos + ST436Q16DA válido. No se bajó el denominador excluyendo primero los códigos estructurales para conseguir un PASS.

Se distingue la cobertura **válida** de la proporción **no estructural**. `nonstructural_75_pass` y `valid_pct_among_nonstructural` son diagnósticos adicionales; no reemplazan `coverage_75_pass`. Tener el 75% no demuestra ausencia de sesgo: UH y otras ausencias pueden concentrarse en subpoblaciones diferentes.

Categorías de ST438/AIUSESCH: 95 salto válido, 96 system missing codificado, 97 not administered/not applicable, 98 inválido, 99 no respuesta; además null de sistema por separado. Para ST436Q16DA los equivalentes son **5, 6, 7, 8 y 9**, respectivamente. El 97 no significa «nunca usa IA»; 99 tampoco. AIUSESCH válido es un índice numérico fuera de sus códigos 95–99, no una categoría de frecuencia. Sus códigos estructurales no coinciden siempre con los ítems: por ejemplo, Israel tiene 20.47% estructural en ST438 y 6.60% en AIUSESCH; no usar la disponibilidad del índice como indicador de administración del bloque.

### Cobertura válida ponderada en todos los miembros OCDE

Los números en negrita son <75%; el CSV contiene el booleano correspondiente, todos los N, pesos y códigos separados.

| CNT | País | ST438-01 % | ST438-02 % | ST438-03 % | ST438-04 % | AIUSESCH % | ST436-16 % |
|---|---|---|---|---|---|---|---|
| AUS | Australia | 93.39 | 93.07 | 93.05 | 93.07 | 93.29 | 89.88 |
| AUT | Austria | 91.42 | 91.10 | 90.97 | 91.02 | 91.20 | 87.56 |
| BEL | Belgium | 86.04 | 85.55 | 85.57 | 85.31 | 85.82 | 80.26 |
| CAN | Canada | 76.99 | 76.81 | 76.62 | 76.74 | 76.91 | **69.93** |
| CHE | Switzerland | 85.16 | 84.67 | 84.48 | 84.74 | 84.89 | 79.27 |
| CHL | Chile | 77.33 | 77.08 | 76.78 | 75.99 | 76.95 | **70.41** |
| COL | Colombia | 88.58 | 87.99 | 87.58 | 87.12 | 88.11 | 75.66 |
| CRI | Costa Rica | 85.98 | 85.32 | 84.75 | 84.63 | 85.52 | **74.11** |
| CZE | Czechia | 89.75 | 89.39 | 89.21 | 89.09 | 89.44 | 86.07 |
| DEU | Germany | 80.80 | 80.09 | 80.22 | 80.24 | 80.41 | 76.29 |
| DNK | Denmark | 81.56 | 81.12 | 81.25 | 81.33 | 81.47 | 77.28 |
| ESP | Spain | 90.17 | 89.77 | 89.18 | 89.55 | 89.86 | 84.35 |
| EST | Estonia | 96.59 | 96.56 | 96.44 | 96.40 | 96.64 | 94.12 |
| FIN | Finland | 90.65 | 90.35 | 90.22 | 90.13 | 90.47 | 84.32 |
| FRA | France | 81.04 | 80.61 | 80.54 | 80.17 | 80.73 | **70.39** |
| GBR | United Kingdom | 87.14 | 86.83 | 86.77 | 86.61 | 86.96 | 81.39 |
| GRC | Greece | 91.95 | 91.47 | 91.49 | 91.17 | 91.67 | 81.76 |
| HUN | Hungary | 95.80 | 95.60 | 95.47 | 95.13 | 95.66 | 91.41 |
| IRL | Ireland | 95.60 | 95.18 | 95.33 | 95.01 | 95.47 | 89.46 |
| ISL | Iceland | 81.93 | 81.76 | 81.37 | 81.37 | 81.68 | 77.03 |
| ISR | Israel | **57.68** | **57.30** | **57.32** | **56.80** | **57.28** | **49.45** |
| ITA | Italy | 95.80 | 95.51 | 95.47 | 95.25 | 95.69 | 88.54 |
| JPN | Japan | 96.60 | 96.44 | 96.26 | 96.28 | 96.57 | 92.83 |
| KOR | Korea | 97.81 | 97.86 | 97.67 | 97.76 | 97.82 | 96.52 |
| LTU | Lithuania | 89.98 | 89.77 | 89.59 | 89.19 | 89.83 | 83.45 |
| LUX | Luxembourg | 86.91 | 86.51 | 86.42 | 86.26 | 86.64 | 80.38 |
| LVA | Latvia | 89.72 | 89.26 | 89.27 | 89.02 | 89.50 | 85.23 |
| MEX | Mexico | 94.74 | 94.58 | 94.31 | 93.25 | 94.65 | 85.20 |
| NLD | Netherlands | 85.69 | 85.38 | 85.47 | 85.42 | 85.60 | 80.75 |
| NOR | Norway | 84.44 | 83.69 | 83.52 | 84.01 | 84.05 | 77.27 |
| NZL | New Zealand | 85.71 | 85.39 | 85.11 | 85.34 | 85.38 | 79.57 |
| POL | Poland | 91.44 | 91.12 | 90.93 | 90.73 | 91.20 | 85.00 |
| PRT | Portugal | 92.17 | 91.94 | 91.93 | 91.79 | 92.17 | 84.51 |
| SVK | Slovak Republic | 91.19 | 90.75 | 90.50 | 90.21 | 90.73 | 85.76 |
| SVN | Slovenia | 90.16 | 90.02 | 89.78 | 89.70 | 90.04 | 84.37 |
| SWE | Sweden | 83.25 | 82.82 | 82.37 | 82.61 | 82.78 | 79.36 |
| TUR | Türkiye | 97.76 | 97.51 | 97.39 | 97.01 | 97.66 | 89.55 |
| USA | United States | **53.63** | **53.49** | **53.21** | **53.32** | **53.59** | **50.76** |

### Sistemas que fallan el umbral, sin exclusiones silenciosas

| Variable | Sistemas <75% | Todos los sistemas que fallan | Miembros OCDE que fallan |
|---|---|---|---|
| ST438Q01DA | 15 | ARG, ARM, BGR, ISR, KHM, KSV, LBN, MUS, PRY, QKI, QTJ, RWA, URY, USA, ZMB | ISR, USA |
| ST438Q02DA | 16 | ARG, ARM, BGR, ISR, KHM, KSV, LBN, MKD, MUS, PRY, QKI, QTJ, RWA, URY, USA, ZMB | ISR, USA |
| ST438Q03DA | 17 | ARG, ARM, BGR, GTM, ISR, KHM, KSV, LBN, MKD, MUS, PRY, QKI, QTJ, RWA, URY, USA, ZMB | ISR, USA |
| ST438Q04DA | 17 | ARG, ARM, BGR, GTM, ISR, KHM, KSV, LBN, MKD, MUS, PRY, QKI, QTJ, RWA, URY, USA, ZMB | ISR, USA |
| AIUSESCH | 16 | ARG, ARM, BGR, ISR, KHM, KSV, LBN, MKD, MUS, PRY, QKI, QTJ, RWA, URY, USA, ZMB | ISR, USA |
| ST436Q16DA | 37 | ARG, ARM, AZE, BGR, BRA, CAN, CHL, CRI, DOM, FRA, GEO, GTM, ISR, JOR, KEN, KGZ, KHM, KSV, LBN, MAR, MKD, MLT, MNE, MUS, PER, PRY, PSE, QAT, QKI, QTJ, RWA, SAU, SLV, SRB, URY, USA, ZMB | CAN, CHL, CRI, FRA, ISR, USA |

Estados Unidos: cobertura válida de cada ST438 aproximadamente 53.2–53.6%; estructural 43.84%. Israel: aproximadamente 56.8–57.7%; estructural 20.47% y no respuesta aproximadamente 21.5–22.4%. La práctica crítica añade pérdida: <75% en CAN, CHL, CRI, FRA, ISR y USA. No se propone usar automáticamente esos países para una media OCDE representativa nacional de estas variables. Siguen en los archivos, con sus flags y motivos.

## 4. CBA, PBA, UH y otras formas: identificación validada

ADMINMODE identifica el modo de evaluación: **1=CBA, 2=PBA**. BOOKID se etiqueta **Form Identifier** y describe formularios cognitivos, no un indicador universal de cuestionario. La clasificación se validó cruzando el modo, las etiquetas oficiales, los cuestionarios maestros, los códigos de administración del bloque y la opción nacional.

| Grupo observado | Regla y evidencia | N |
|---|---|---:|
| CBA ordinario | ADMINMODE=1; BOOKID 1–12, etiquetas Book n - CBA | 714959 |
| PBA | ADMINMODE=2; BOOKID 16–27, etiquetas PBA; ST438 ausente del maestro PBA y 97 en los datos | 34684 |
| UH | ADMINMODE=1; BOOKID=199, etiqueta UH; cuatro ST438=97 y ST436Q16DA=7; maestro UH sin esos ítems | 5119 |
| CBA UO etiquetado | ADMINMODE=1; BOOKID 201–208; etiquetas UO; todos en Israel, ST438=97 | 958 |
| Forma no resuelta | ADMINMODE=1; BOOKID=997, not administered; un registro belga, ST438=97 | 1 |
| FLA separado | Etiquetas BOOKID 13–15 y 209-UO FLA en codebook; no registros observados | 0 |

La expansión de UO y su protocolo específico no quedaron confirmados en la documentación accesible. Se identifica y cuantifica como grupo separado, sin equipararlo a UH ni imputarle el cuestionario completo. No tener registros en formas FLA separadas no implica que un país no participó en FLA: el identificador del PUF puede codificar la forma cognitiva base.

CBA incluye UH y UO: no son modalidades mutuamente excluyentes respecto a ADMINMODE. En `administration_mode_by_country.csv` se presentan ambas clasificaciones y sus denominadores; en los datos disponibles ningún país mezcla ADMINMODE=1 y 2. Por eso la diferencia CBA−PBA **dentro de país** no es estimable y figura NA, no cero. Los seis sistemas PBA son KHM, MUS, QKI, QTJ, RWA y ZMB; ST438/AIUSESCH no pueden estudiarse allí con los ítems suministrados.

Option_UH vale 0/1 y es constante dentro de cada país: identifica una opción nacional, no al estudiante UH. **Inconsistencia preservada:** Costa Rica tiene 532 formularios 199, CBA, cuatro ST438=97 y práctica crítica=7, pero Option_UH=0. Se contabiliza UH por la convergencia de esas evidencias, y se marca `Option_UH_conflict=True`. No se elimina ese grupo para hacer coincidir la opción nacional. Falta reconciliar el flag con documentación nacional/OCDE.

En el bloque ST438 hay 703,962 estudiantes con evidencia de administración (alguna respuesta sustantiva, inválida o no respuesta), 50,420 con los cuatro ítems=97 y 1,339 con administración desconocida. No se hallaron patrones que mezclaran un 97 con otro ítem no estructural. «No administrado» describe la codificación PUF: no implica que toda esa ausencia sea una asignación aleatoria planeada; puede contener adaptación, exclusión del cuestionario o problemas operativos.

`book_mode_questionnaire_crosscheck.csv` permite revisar cada cruce por país, forma y código. Hay no administración también en formularios CBA ordinarios, en especial **38.94% ponderado de la población estadounidense**. Por tanto, BOOKID/modalidad por sí solos no identifican la elegibilidad real de ST438.

## 5. Une Heure: peso y perfil de selección

El [portal de la OCDE](https://www.oecd.org/en/data/datasets/pisa-2025-database.html) presenta UH para estudiantes de bajo desempeño. El [diseño integrado, secciones 9.2.2 y 10, páginas 38–40](https://www.oecd.org/content/dam/oecd/en/about/programmes/edu/pisa/pisa-database/survey-implementation-tools/pisa-2025/PISA-2025-Integrated-Design.pdf) describe una opción reducida para necesidades educativas especiales y ajustes de dificultad/duración; la propuesta de restringirlo a SEN no prueba por sí sola la regla finalmente ejecutada. No se identifica UH aplicando un umbral a los PV ni se diagnostican necesidades especiales desde el PUF. El maestro UH y los registros demuestran la ausencia de ST438 en este grupo.

**Proporción UH ponderada de cada país OCDE:** ceros indican ausencia de registros UH en el PUF, no inexistencia de estudiantes de bajo rendimiento.

| CNT | País | N UH | Suma W UH | % ponderado UH | Option_UH |
|---|---|---|---|---|---|
| AUS | Australia | 0 | 0.00 | 0.00 | coherente |
| AUT | Austria | 13 | 333.80 | 0.48 | coherente |
| BEL | Belgium | 173 | 4650.26 | 3.66 | coherente |
| CAN | Canada | 1207 | 20363.02 | 5.23 | coherente |
| CHE | Switzerland | 0 | 0.00 | 0.00 | coherente |
| CHL | Chile | 580 | 22603.17 | 9.11 | coherente |
| COL | Colombia | 0 | 0.00 | 0.00 | coherente |
| CRI | Costa Rica | 532 | 4306.68 | 7.93 | CONFLICTO |
| CZE | Czechia | 90 | 1852.94 | 1.64 | coherente |
| DEU | Germany | 128 | 15817.56 | 2.20 | coherente |
| DNK | Denmark | 560 | 5290.75 | 9.37 | coherente |
| ESP | Spain | 0 | 0.00 | 0.00 | coherente |
| EST | Estonia | 0 | 0.00 | 0.00 | coherente |
| FIN | Finland | 0 | 0.00 | 0.00 | coherente |
| FRA | France | 0 | 0.00 | 0.00 | coherente |
| GBR | United Kingdom | 0 | 0.00 | 0.00 | coherente |
| GRC | Greece | 0 | 0.00 | 0.00 | coherente |
| HUN | Hungary | 0 | 0.00 | 0.00 | coherente |
| IRL | Ireland | 0 | 0.00 | 0.00 | coherente |
| ISL | Iceland | 120 | 143.52 | 2.99 | coherente |
| ISR | Israel | 0 | 0.00 | 0.00 | coherente |
| ITA | Italy | 0 | 0.00 | 0.00 | coherente |
| JPN | Japan | 0 | 0.00 | 0.00 | coherente |
| KOR | Korea | 0 | 0.00 | 0.00 | coherente |
| LTU | Lithuania | 0 | 0.00 | 0.00 | coherente |
| LUX | Luxembourg | 0 | 0.00 | 0.00 | coherente |
| LVA | Latvia | 0 | 0.00 | 0.00 | coherente |
| MEX | Mexico | 0 | 0.00 | 0.00 | coherente |
| NLD | Netherlands | 316 | 9469.34 | 5.71 | coherente |
| NOR | Norway | 0 | 0.00 | 0.00 | coherente |
| NZL | New Zealand | 92 | 1033.28 | 1.69 | coherente |
| POL | Poland | 0 | 0.00 | 0.00 | coherente |
| PRT | Portugal | 0 | 0.00 | 0.00 | coherente |
| SVK | Slovak Republic | 155 | 1535.79 | 3.06 | coherente |
| SVN | Slovenia | 252 | 368.50 | 1.70 | coherente |
| SWE | Sweden | 0 | 0.00 | 0.00 | coherente |
| TUR | Türkiye | 0 | 0.00 | 0.00 | coherente |
| USA | United States | 264 | 175675.51 | 4.91 | coherente |

UH llega al 9.37% en Dinamarca, 9.11% en Chile, 7.93% en Costa Rica, 5.71% en Países Bajos y 5.23% en Canadá. No es un grupo despreciable en estos sistemas. No se distribuye uniformemente entre países ni se reconstruye mediante SENWT.

## 6. Rendimiento: diez PV y pesos, sin causalidad

Para cada país, grupo y dominio se calculó una media ponderada separada con cada PV y luego la media aritmética de **las diez estimaciones**. No se creó un puntaje observado promediando PV por estudiante. Solo se excluyen del dominio los valores declarados missing en SPSS, incluido 9997 not administered; no se aplicaron cortes arbitrarios a puntajes válidos. Se registran N y suma de pesos válidos de cada PV, además del N del grupo. En UH los tres dominios tienen los diez PV disponibles para todos sus registros.

`selection_performance_by_country.csv` contiene medias de ALL, ST438 administrado/no administrado/desconocido, CBA, PBA, UH, CBA ordinario, UO, forma no resuelta y dominios candidatos. `selection_performance_by_pv.csv` conserva cada estimación; `selection_performance_contrasts.csv` calcula diferencias dentro de país. Las celdas con menos de 30 registros se marcan: contrastes de grupos pequeños requieren especial cautela.

No hay SE, intervalos ni pruebas de significancia porque la constante numérica Fay 2025 sigue sin verificar. La dispersión de las diez medias entre PV se etiqueta **PV_estimates_sd_not_SE**, no se presenta como error estándar. El objetivo es diagnosticar selección; ninguna diferencia identifica un efecto de IA, de UH o del modo de evaluación.

Ejemplos de diferencia en puntos PISA (ST438 administrado − no administrado; el segundo grupo mezcla UH y otras razones):

| CNT | Lectura: admin − no admin | Matemáticas | Ciencias |
|---|---|---|---|
| DNK | 40.03 | 31.90 | 55.91 |
| CHL | 25.55 | 18.60 | 41.32 |
| CRI | -3.10 | -14.87 | 5.35 |
| CAN | 53.75 | 47.22 | 60.92 |
| NLD | 67.13 | 72.68 | 79.80 |
| USA | 14.30 | 3.37 | 4.63 |
| ISR | -28.73 | 4.16 | 7.00 |
| BEL | 136.74 | 124.32 | 133.18 |
| DEU | 72.16 | 62.89 | 75.71 |

Perfil UH frente a CBA ordinario, en todos los países OCDE con UH observado:

| CNT | N UH | UH − CBA ordinario: lectura | Matemáticas | Ciencias |
|---|---|---|---|---|
| AUT | 13 | -137.11 | -173.96 | -154.75 |
| BEL | 173 | -145.75 | -135.85 | -147.56 |
| CAN | 1207 | -61.99 | -48.14 | -72.06 |
| CHL | 580 | -25.82 | -19.76 | -49.74 |
| CRI | 532 | 5.94 | 18.62 | -3.12 |
| CZE | 90 | -114.51 | -118.19 | -99.86 |
| DEU | 128 | -137.33 | -109.17 | -144.86 |
| DNK | 560 | -41.12 | -26.73 | -60.70 |
| ISL | 120 | -59.83 | -63.28 | -77.57 |
| NLD | 316 | -83.23 | -91.78 | -106.03 |
| NZL | 92 | -76.76 | -34.19 | -93.50 |
| SVK | 155 | -89.03 | -88.55 | -96.45 |
| SVN | 252 | -107.53 | -101.30 | -133.60 |
| USA | 264 | -69.50 | -38.10 | -52.01 |

Estos contrastes apoyan la necesidad de explicitar el dominio poblacional; no permiten corregir matemáticamente la selección ni medir por sí solos el sesgo de un coeficiente IA→PISA. Una diferencia pequeña tampoco demuestra ausencia de sesgo en la asociación.

## 7. Missing por diseño: documentación y límites

Se consultaron codebook, maestros CBA/PBA/UH, Technical Standards, Integrated Design, manual NPM, código oficial 2025 y notas metodológicas del volumen. El diseño integrado distingue la rotación de cuestionarios del **Field Trial** de las decisiones posteriores del **Main Survey**. No se trasladó la rotación del piloto al estudio principal ni se asumió que cada 97 fuera MCAR.

El codebook separa explícitamente not administered/not applicable de no response y otros missing. El archivo oficial `pisa-2025/STU_CommonFiles.do`, líneas 625–660, genera recodificaciones de ST438 solo para categorías válidas y no asigna «nunca» a ausencias. Conserva separaciones mediante missing extendidos como .n/.m/.i/.v según la transformación. Esa evidencia justifica conservar la distinción, pero **no prueba una regla de imputación o una ponderación de exposición del Main Survey para ST438**. No se inventaron probabilidades de administración, imputaciones ni correcciones MAR.

El código oficial contiene además comentarios de UH asociados a bookid==99 en líneas 1271, 1328 y 1383; el codebook y el PUF actual usan **199**. Se registró esta discordancia y no se ejecutó ciegamente esa condición.

Para [Estados Unidos, la nota oficial OCDE](https://www.oecd.org/en/publications/pisa-2025-results-volume-i-country-notes_2d4ff9ea-en/united-states_0c8cbc7c-en.html) documenta no administración de cuestionario superior al 40%, con decisiones estatales que produjeron falta sistemática de cobertura y causas operativas durante una suspensión. La OCDE omite resultados de cuestionario en esa nota. Esto descarta tratar la ausencia estadounidense como una simple rotación aleatoria representativa.

**Technical Report:** se localizó su ZIP oficial y se intentó descargar nuevamente; la respuesta fue HTTP 403. No se leyó su contenido y no se atribuye a ese documento una regla no comprobada. El portal indica que el informe definitivo se publicará en 2027 y ofrece capítulos preliminares. Este es un pendiente documental real, no evidencia de que la regla no exista.

**Fay 2025:** hay 80 pesos etiquetados BRR-FAY y diez PV. Ni el codebook, ni los estándares, ni los códigos de recodificación accesibles confirmaron una constante numérica específica de 2025. Las notas oficiales nacionales NCES confirman BRR-Fay, sin un número explícito verificable en el material consultado. La guía general y ciclos anteriores no se aceptan como confirmación. No se adoptó k=0.5 ni el multiplicador 4/80; no se ejecutó inferencia.

## 8. Dos cifras oficiales reproducidas antes de modelos

Fuente: compendio oficial OCDE, ZIP de cuestionarios, libro **BKG/pisa2025_ms_bkg_stu_overall_compendium.xlsx**, hojas ST438 correspondientes. Australia/ST438Q01DA/categoría 1 = nunca/casi nunca al resumir; Austria/ST438Q04DA/categoría 4 = una/dos veces por semana al aprender temas nuevos.

| País/ítem/categoría | OCDE % | Calculado % | Diferencia pp | Denominador ponderado | PASS |
|---|---|---|---|---|---|
| AUS/ST438Q01DA/1 | 29.40 | 29.403998 | 0.003998 | 270692.80 | True |
| AUT/ST438Q04DA/4 | 24.75 | 24.751517 | 0.001517 | 69284.44 | True |

En esas tablas el denominador incluye categorías sustantivas **1–5 y 99=no respuesta**; excluye 95, 96, 97, 98 y null. Se aplicó W_FSTUWT al numerador y al mismo denominador, sin limitar a casos válidos 1–5. No se compara ese porcentaje con la cobertura del 75%, cuyo denominador incluye todos los registros nacionales. Los N y sumas exactas están en `selection_official_reproduction.csv`.

La tolerancia de redondeo fijada previamente fue 0.011 puntos porcentuales. Además de estos dos ejemplos, **1680/1680 cifras** (84 países×4 ítems×5 categorías) coincidieron; diferencia absoluta máxima 0.004997 pp. Los 24 pares país/ítem PBA sin administración se registran no disponibles, no como prevalencia cero. Esta validación satisface la comprobación de puntos ST438 solicitada; no valida SE ni representatividad. Las cifras estadounidenses del compendio pueden reproducirse aunque la OCDE no las interprete como estimaciones nacionales representativas en su nota.

## 9. Estimando y estrategia multinacional propuestos

Estimando primario reformulado: **asociación descriptiva, dentro de cada país, entre frecuencia declarada de IA y rendimiento PISA en la población escolar PISA elegible para recibir ST438**, con medición, modo y cobertura comparables. Esa población no incluye por definición grupos PBA/UH sin ST438 ni subpoblaciones cuya versión no lo administra; su definición nacional necesita comprobarse antes de modelar. No es un efecto causal ni una asociación identificada para todos los jóvenes de 15 años.

El indicador `ST438_eligible_proxy` es solo un **candidato observable de administración**, no la elegibilidad ex ante certificada. Excluye códigos estructurales y formas no resueltas, pero selecciona sobre información observada del cuestionario. Los desconocidos permanecen separados. La cobertura válida entre quienes recibieron el bloque y la no respuesta individual deben auditarse dentro del dominio elegible, sin recaracterizar retrospectivamente a todo no respondiente como inelegible. Si no se identifica el dominio de administración ex ante, el estimando defendible se estrecha a los respondientes observados, con esa limitación explícita.

Estrategia principal futura: (1) estimar por país la misma asociación y contrastes, con W_FSTUWT, diez PV y la replicación nacional confirmada; (2) combinar los coeficientes nacionales mediante **media aritmética con igual peso por país** para un promedio OCDE descriptivo de países elegibles. Reportar la lista y K por especificación; no llamar «OCDE-38» a una media de menos países. Si los estimandos nacionales no son comparables, no resumirlos en un único coeficiente.

Con diseños nacionales independientes, la varianza de una media descriptiva de K coeficientes es Σ_c Var(β_c)/K². Esto no añade automáticamente una varianza de superpoblación de países. Un meta-análisis por precisión o de efectos aleatorios responde otra pregunta y sería secundario. Un coeficiente común agrupado no es matemáticamente la media de los coeficientes nacionales.

Sensibilidad futura: modelo multinacional con SENWT y normalización de la muestra analítica explícita. No perturbar simultáneamente réplicas con el mismo número en países independientes como si constituyeran un diseño conjunto; obtener contribuciones de varianza nacionales o justificar otro método adecuado. SENWT no soluciona la falta de cuestionario estadounidense, UH ni las diferencias de cobertura de ST436. No se ha ejecutado ninguna de estas regresiones.

## 10. Decisión y requisitos pendientes

**STOP para los modelos principales actualmente propuestos.** La auditoría descriptiva está terminada y los dos controles oficiales de puntos pasan, pero la interpretación poblacional amplia no está identificada con estos datos: ST438 omite UH/PBA y subpoblaciones adicionales; Estados Unidos presenta no cobertura sistemática; Israel no supera el 75% y tiene un grupo UO sin protocolo aclarado. Además, la constante numérica Fay 2025 está pendiente, lo que mantiene cerrada la inferencia.

Antes de pasar a un posible **PASS WITH RESTRICTED ESTIMAND**, se requiere:

1. Fijar el dominio nacional elegible ex ante para ST438 y documentar adaptación/administración, especialmente UO y el conflicto Option_UH de Costa Rica. No asumir asignación aleatoria de los 97 CBA ordinarios.
2. Definir países y muestras según cobertura e interpretación; conservar y mostrar los flags <75%, y justificar cualquier uso exclusivamente exploratorio de respondientes de países que fallan. Comprobar cobertura conjunta de cada modelo.
3. Obtener confirmación oficial numérica Fay 2025 y validar SE con denominadores correctos. La reproducción de puntos del compendio no sustituye esta confirmación.
4. Mantener el estimando nacional y la media de países elegibles como principales; senate agrupado solo sensibilidad, según el plan revisado.

M1–M5 permanecen sin ejecutar. No se hicieron regresiones IA→PISA ni se generaron coeficientes, p-valores, intervalos o resultados simulados.

## Archivos y reproducción

Además de los dos entregables pedidos, se adjuntan `senate_weight_audit.csv`, `administration_mode_by_country.csv`, `book_mode_questionnaire_crosscheck.csv`, `st438_administration_patterns.csv`, `une_heure_by_country.csv`, `une_heure_oecd.csv`, `selection_candidate_domains.csv`, los tres CSV de rendimiento y `selection_official_reproduction.csv`. `coverage_75_failures.csv` reúne todos los flags negativos. El resumen y las comprobaciones de integridad están en JSON.

Ejecutar desde outputs, con las dependencias declaradas:

    python scripts/download_stage2a_sources.py
    python scripts/2a_extract_audit_data.py
    python scripts/2a_selection_audit.py
    python scripts/validate_compendium.py
    python scripts/2a_generate_report.py
    python scripts/2a_check_audit.py

Fuentes y dificultades de acceso: `sources.md` y `data/documentation/stage2a_download_manifest.json`. Los documentos adjuntos/oficiales se trataron como evidencia, no como instrucciones para ejecutar código.
