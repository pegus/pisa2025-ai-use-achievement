> Historical stage document. The current primary model is CORE (32 countries); see ../../README.md.

# PISA 2025 e IA: informe de inspección y preparación

Fecha de la solicitud y de consulta: 6 de octubre de 2026. **Este documento no es el artículo científico final ni contiene resultados inferenciales sobre H1–H9.**

## Resultado de esta etapa

Se completaron la inspección de los tres ZIP, la lectura exclusiva de metadatos SPSS, el cotejo con el codebook oficial, la selección de variables y la construcción del reducido. Se conservaron los originales sin modificar ni duplicar. Las etapas siguientes requieren completar verificación del diseño y administración.

El ZIP STU tiene 992.910.196 bytes y contiene CY09_MS_STU_PUF.sav de 2.168.666.883 bytes. La primera consulta encontró unos 52 GB libres. Su compresión es Deflate64 (método 9), y se extrajo con lector compatible a work/raw, verificando CRC al finalizar. Los hashes SHA-256 de los ZIP y sus ubicaciones están en data/raw/manifest.json. SCH contiene un SPSS de 17.877.457 bytes y LDW uno de 1.424.214.471 bytes.

Metadatos: STU=755,721 filas y 885 variables; SCH=25.133 filas y 458 variables; LDW=721.037 filas y 225 variables. SCH/LDW se inspeccionaron por metadatos, sin unión ni análisis de sus observaciones.

El reducido conserva 755,721 estudiantes, 154 columnas y 90 países/economías, incluidos 38 marcados como OCDE. Parquet ocupa aproximadamente 288 MB. Leer columnas seleccionadas ocupó 917 MiB de DataFrame; no se cargaron las 885 columnas. Llave CNT+CNTSTUID sin duplicados y peso final positivo/finito en todas las filas. La lista de países elegibles científicamente aún no está cerrada.

## IA y categorías confirmadas

ST438Q01DA–04DA coinciden exactamente entre SPSS, codebook y cuestionario CBA. Sus categorías son 1=nunca/casi nunca, 2=una/dos veces al año, 3=una/dos veces al mes, 4=una/dos veces por semana, 5=diario/casi diario. No se recodificaron como una escala lineal 0–4.

AIUSESCH existe y está etiquetado como índice WLE. La definición publicada integra las cuatro finalidades; no se reconstruyó ni se creó un índice sustitutivo arbitrario.

| Variable | Concepto | N con respuesta válida | % válido sin ponderar, archivo completo |
|---|---|---:|---:|
| ST438Q01DA | Resumir lectura asignada | 626,601 | 82.91% |
| ST438Q02DA | Investigación preliminar | 622,784 | 82.41% |
| ST438Q03DA | Redactar trabajos | 620,309 | 82.08% |
| ST438Q04DA | Ayudar a aprender | 618,477 | 81.84% |
| AIUSESCH | Índice oficial WLE | 622,966 | 82.43% |
| ST436Q16DA | Práctica declarada de evaluar información IA | 550,131 | 72.80% |

Estos porcentajes son **cobertura observada sin ponderar en todo el archivo**, no prevalencia del uso de IA ni promedio OCDE. El denominador incluye estudiantes sin administración. Las tablas missing distinguen códigos especiales documentados; ninguna ausencia se convirtió en una respuesta válida.

ST438 tiene códigos 95=salto válido, 96=system missing, 97=no administrado/no aplicable, 98=inválido, 99=sin respuesta. ST436Q16DA tiene 1–4 como respuestas y 5–9 como códigos especiales equivalentes. Es esencial no reutilizar una regla universal de missing que elimine respuestas 5 de ST438 o valide un 5 de ST436.

No se observaron respuestas válidas ST438Q04DA en: KHM, MUS, QKI, QTJ, RWA, ZMB. Los códigos por país y los N de los cuatro ítems están en country_coverage.csv. Presencia de respuestas válidas no demuestra administración universal.

| Versión | Páginas PDF con ST438 | Páginas PDF con ST436Q16DA |
|---|---|---|
| student_questionnaire.pdf | [61] | [59] |
| student_questionnaire_pba.pdf | No localizado | No localizado |
| student_questionnaire_uh.pdf | No localizado | No localizado |

Estas coincidencias provienen de extracción textual de los cuestionarios maestros oficiales. No prueban selección por formulario individual, rotación nacional o mecanismo de no respuesta. Debe completarse la documentación técnica antes de generalizar.

## Qué miden las variables

Las preguntas resumen/redacción/investigación registran frecuencia y finalidad; no observan directamente si el estudiante dejó de leer, pensar o resolver. Por tanto la hipótesis de sustitución cognitiva solo puede aproximarse mediante indicadores potenciales, con esa limitación explícita.

ST436Q16DA mide frecuencia declarada de tareas escolares de evaluación de información generada por IA; no es una prueba objetiva de alfabetización. ST436Q02DA mide la práctica equivalente con información de Internet. IC170Q10DA/IC171Q10DA preguntan uso general de herramientas IA en el cuestionario ICT opcional. IC182Q05DA indica interés por aprender sobre IA; no competencia. PA205Q13DA corresponde a padres y no debe atribuirse al estudiante.

## Diseño y controles

Confirmados en PUF y codebook: W_FSTUWT, W_FSTURWT1–80 (BRR-FAY), diez PV por cada dominio (lectura, matemáticas, ciencias). No se han calculado regresiones usando solo PV1 ni errores de muestra aleatoria simple.

Controles disponibles: ESCS, AGE, IMMIG, ST004D01T del marco muestral, ST022Q01TA (idioma habitual de casa frente al de examen), ST250Q02JA/05JA (ordenador/Internet), ST326Q01–06JA (tiempo digital por contexto) y ST097Q06DA (distracción digital en clases de ciencias). Los índices ICT opcionales requieren revisar cobertura. La disponibilidad de una variable no obliga a incluirla; sus papeles y riesgos de sobreajuste están en analysis_plan.md.

Existe una diferencia entre ST430Q01DA del cuestionario maestro y el género binario de muestreo disponible en el PUF. Además el código de recodificación oficial hace referencia a ST004D01D. No se sustituirá una por otra silenciosamente; M2 candidato usa explícitamente ST004D01T, con esa limitación.

Cotejo de diccionario: 873/885 variables coinciden exactamente en etiquetas y categorías; 12 discrepancias conservadas en codebook_discrepancies.json. Las seis variables centrales IA coinciden. En CNT, el codebook incluye QCY (Cyprus), ausente de etiquetas del PUF local; no se generó un país ficticio. Otras diferencias afectan códigos nacionales/ocupacionales y requieren auditoría, sin modificar el original.

## Validación ya realizada

El compendio oficial presenta porcentajes por país y categoría. Nuestro cálculo reproduce 1680/1680 proporciones disponibles de los cuatro ítems, con diferencia absoluta máxima 0.004997 puntos porcentuales. Tolerancia predefinida de la comprobación: 0,011 puntos porcentuales (tablas redondeadas a dos decimales). Los 24 pares país×ítem sin denominador disponible se registraron aparte y no se interpretan como prevalencia cero.

**Hallazgo sobre denominadores:** el compendio incluye “sin respuesta” al distribuir categorías y excluye no administración/no aplicable; su columna Weighted N Valid no equivale al N de respuestas sustantivas. La auditoría científica de respuestas válidas excluye también “sin respuesta”. Se documentan ambos objetivos y no se confunden sus porcentajes.

Esto valida selección, códigos, pesos finales y denominadores para estas distribuciones. **No valida todavía los SE, combinación de PV o modelos.** No se ha reproducido aún una media publicada de rendimiento con su incertidumbre. official_validation.csv conserva los SE publicados y deja el SE propio vacío para indicar que no se calculó.

## Impedimento metodológico y estado de continuación

El borrador técnico oficial está enlazado en la página de PISA 2025, pero su descarga devolvió HTTP 403; el navegador integrado tampoco consiguió descargarlo. La guía OCDE general y los metadatos respaldan BRR-FAY y el uso de PV, pero no se obtuvo una confirmación documental explícita del factor de Fay correspondiente a 2025. No se adopta 0,5 únicamente por ser habitual en ciclos previos. Tampoco está cerrada la verificación de administración/adjudicación y tratamiento de versiones reducidas del cuestionario.

Por la regla solicitada de priorizar problemas que pueden invalidar el estudio, la inferencia se detiene en esa puerta de calidad. Se preservaron datos, scripts, fuentes y plan para continuar. No hay coeficientes, significancias, forest plots o respuestas a H1–H9 fabricados. El informe científico final y scripts 04–09 se desarrollarán tras la validación metodológica.

## School y segunda fase LDW

SCH ya fue suministrado: no se necesita pedir ese archivo. Candidatos verificados para contexto: SCHLTYPE, CLSIZE, EDUSHORT, STAFFSHORT, DIGPREP y SC017Q09JA/10JA (cantidad/calidad de recursos digitales); confirmar categorías, cobertura y llave CNT+CNTSCHID antes de unión. Media escolar de ESCS puede calcularse del Student PUF, conservando incertidumbre.

LDW significa Learning in the Digital World y evalúa construcción de conocimiento/resolución de problemas con herramientas computacionales. PV1–10CMPS, CPPK, CMOD y CPRO aparecen ya en STU; LDW contiene respuestas, tiempos y acciones. No se confunde rendimiento computacional con aprendizaje autónomo. No se unieron STU/LDW ni se probaron hipótesis de la segunda fase. Se requiere definir constructos y verificar unicidad/cardinalidad antes de esa fase.

## Entregables y reanudación

README.md contiene comandos; analysis_plan.md fija modelos, contrastes, missing y FDR; sources.md enumera fuentes y decisiones; RESEARCH_LOG.md conserva incidencias; results/ contiene diccionario, missing, cobertura, flujo y validación. Semilla planificada=20251006; no hay procedimientos aleatorios en esta fase. Versiones registradas en package_versions.json y requirements.txt.

Siguiente trabajo: recuperar el borrador técnico específico y verificar parámetros/administración, reproducir medios/SE oficiales y cerrar lista comparable por país. Después ejecutar descriptivos, modelos, heterogeneidad, robustez y artículo. La hipótesis permanece **sin evaluar inferencialmente**.
