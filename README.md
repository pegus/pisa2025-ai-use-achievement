# Entre apoyo y automatización: uso de inteligencia artificial y rendimiento en PISA 2025

**Reproducible analysis of generative AI use and student achievement in PISA 2025**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23326121.svg)](https://doi.org/10.5281/zenodo.23326121) [![Release](https://img.shields.io/github/v/release/pegus/pisa2025-ai-use-achievement)](https://github.com/pegus/pisa2025-ai-use-achievement/releases/tag/v1.0.0) [![Checks](https://github.com/pegus/pisa2025-ai-use-achievement/actions/workflows/checks.yml/badge.svg)](https://github.com/pegus/pisa2025-ai-use-achievement/actions/workflows/checks.yml) [![Python](https://img.shields.io/badge/Python-3.12-blue)](requirements.txt) [![License MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

Software y resultados agregados del estudio de Pedro Gustavo González Ali ([ORCID](https://orcid.org/0000-0003-0630-8703)). Este repositorio permite auditar los análisis secuenciales de cobertura, diseño muestral y robustez. Todos los resultados se interpretan como **asociaciones**. No redistribuye microdatos ni pesos individuales.

## Preguntas de investigación

¿Cómo se relacionan la frecuencia y finalidad declaradas del uso de IA con lectura, matemáticas y ciencias? ¿Persisten los patrones al ajustar contexto familiar, escuela y acceso/comportamientos digitales? ¿Existe especificidad por dominio? ¿Cuánto cambian los resultados según cobertura y país?

## Datos, muestra y variables

[OCDE PISA 2025](https://www.oecd.org/en/data/datasets/pisa-2025-database.html), PUF estudiantil SPSS `CY09_MS_STU_PUF.zip`: 755.721 estudiantes, 90 países/economías y 38 sistemas marcados OCDE. Auditoría de los cuatro ST438 >=75%: 36 candidatos; USA/ISR fuera del conjunto principal. **Modelo principal M2-CORE: ESCS + IMMIG + ST022Q01TA; síntesis de 32 países** con cobertura conjunta >=75%. M2-FULL añade sexo y edad donde existen: 21 países, **sensibilidad**, no especificación principal equivalente. FE CORE: 30 países (identificador escolar ausente en ISL/LUX); FE FULL: 21. Las muestras varían por contraste/modelo y se identifican en cada tabla.

ST438Q01DA=resumir, Q02=investigación preliminar, Q03=redactar, Q04=ayudar a aprender. Categorías: nunca/casi nunca; una/dos veces al año; una/dos veces al mes; una/dos veces por semana; diario/casi diario. Se modelan con indicadores, sin intervalos equidistantes. Resultados: `PV1–PV10READ/MATH/SCIE`. [Diccionario](docs/VARIABLE_DICTIONARY.csv) y [codebook](CODEBOOK.md).

## Diseño estadístico

Modelos nacionales separados, `W_FSTUWT`, 80 pesos replicados `W_FSTURWT1–80`, BRR-Fay k=.5. Cada PV se estima separadamente; **ningún promedio de PV por estudiante**. Se combinan estimaciones y varianzas: Ū + (1+1/10)B. Promedio multinacional principal: coeficientes nacionales con igual peso, varianza ΣT/K². No se trata la réplica r de países independientes como un diseño multinacional conjunto. SENWT se conserva/verifica como 5000 W/suma nacional; un modelo multinacional SENWT no fue estimado y no se presenta como evidencia producida. [Detalles](docs/PISA_SURVEY_DESIGN.md).

## Hallazgos y límites

La asociación del uso diario para resumir y redactar con el rendimiento es negativa y persiste con FE escolar y acceso digital. Diario generalmente obtiene un contraste negativo frente a semanal. Existe heterogeneidad considerable entre países. El patrón de ayudar a aprender difiere, pero su firma inicial cambia con FE. Los controles digitales actuales atenúan ciertos contrastes y tienen orden temporal ambiguo. La especificidad lectura–ciencias no es robusta en FULL. **La explicación específica de sustitución cognitiva permanece indeterminada frente a selección/causalidad inversa.**

Estimando restringido a respondientes ST438 con covariables observadas en los sistemas elegibles; no automáticamente todos los jóvenes de 15 años. Sin identificación causal, ni rendimiento previo individual ni fecha de adopción de IA. La validación de 18 medias/SE oficiales confirma empíricamente k=.5, pero no sustituye todos los capítulos del Technical Report 2025 cuyo borrador no pudo leerse completo en la investigación. No análisis LDW ni artículo final en esta release.

## Estructura e instalación

`scripts/legacy/`: cálculos originales con adaptaciones explícitas; `scripts/pipeline.py`: controlador portátil. `docs/history/`: planes, informes y bitácora secuenciales; `results/aggregated`, `robustness`, `validation`: productos nacionales/internacionales; `figures/`: seis PNG y PDF de 60 páginas; `tests/`: comprobaciones públicas. Resultados individuales/intermedios solo en `.reproduction/`, ignorada por Git.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/00_check_environment.py
```

Python de referencia: 3.12.14; versiones utilizadas están fijadas en requirements.txt. Se recomienda >=8 GB RAM y >=10 GB de disco libre. No se descargan gigabytes silenciosamente. Véase [REPRODUCIBILITY.md](REPRODUCIBILITY.md).

## Descargar datos y reproducir

Descargue personalmente el Student SPSS PUF oficial y sitúe `CY09_MS_STU_PUF.zip` en `data/raw/`. [Instrucciones y checksum](data/README.md).

```bash
python scripts/11_reproduce_all.py
# Ruta alternativa:
python scripts/11_reproduce_all.py --puf /ruta/CY09_MS_STU_PUF.zip
```

Para pasos separados, siempre en este orden:

```bash
python scripts/11_reproduce_all.py --stage prepare
python scripts/11_reproduce_all.py --stage selection
python scripts/11_reproduce_all.py --stage validation
python scripts/11_reproduce_all.py --stage main
python scripts/11_reproduce_all.py --stage diagnostics
python scripts/11_reproduce_all.py --stage digital
python scripts/11_reproduce_all.py --stage synthesis
python scripts/11_reproduce_all.py --stage verify
python scripts/11_reproduce_all.py --stage figures
python scripts/11_reproduce_all.py --stage report
python -m unittest discover -s tests -v
```

FE y modelos conjuntos forman parte del mismo motor de `main`: conservamos su secuencia real en vez de crear nombres de scripts que aparenten análisis separados. La reproducción no modifica las tablas de referencia publicadas. La supresión de celdas pequeñas se aplica solo a la copia pública, no a cálculos locales.

## Cita, licencia, IA y contacto

Use [CITATION.cff](CITATION.cff) y [CITATION_FOR_MANUSCRIPT.md](CITATION_FOR_MANUSCRIPT.md). Archivo permanente en Zenodo: [DOI conceptual](https://doi.org/10.5281/zenodo.23326121) y [DOI de la versión 1.0.0](https://doi.org/10.5281/zenodo.23326122). La versión científica está fijada al commit `37769e72d80f8e52487a49a532c49471c5c85bb4`. [Verificación del archivo y decisión sobre metadatos](docs/ARCHIVAL_METADATA.md).

MIT cubre el código y documentación originales del investigador. Metadatos de variables y cifras oficiales de OCDE conservan sus derechos y atribución: esta licencia no modifica las condiciones de microdatos ni de materiales de terceros. [Condiciones OCDE](https://www.oecd.org/en/about/terms-conditions.html).

Codex asistió el procesamiento, programación, inferencia, validación y documentación; ChatGPT apoyó discusión metodológica y edición, según declaración del investigador. La supervisión y responsabilidad científica corresponden al autor; IA no es autora. [Declaración completa](docs/AI_USE_DISCLOSURE.md).

Contacto público: [issues del repositorio](https://github.com/pegus/pisa2025-ai-use-achievement/issues). No se publica correo privado.
