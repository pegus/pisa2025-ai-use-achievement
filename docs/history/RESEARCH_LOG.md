> Historical stage document. The current primary model is CORE (32 countries); see ../../README.md.


## 2026-10-06T09:46:05.299993-05:00
- Análisis: Documentación OCDE descargada
- Resultado: [{'file': 'database.html', 'url': 'https://www.oecd.org/en/data/datasets/pisa-2025-database.html', 'status': 'HTTP Error 403: Forbidden'}, {'file': 'codebook.xlsx', 'url': 'https://webfs.oecd.org/pisa2022/2025/PISA2025_Codebook.xlsx', 'status': 'downloaded', 'bytes': 985161}, {'file': 'technical_report.zip', 'url': 'https://www.oecd.org/content/dam/oecd/en/about/programmes/edu/pisa/publications/technical-report/PISA%202025%20Technical%20Report.zip', 'status': 'HTTP Error 403: Forbidden'}, {'file': 'student_questionnaire.pdf', 'url': 'https://www.oecd.org/content/dam/oecd/en/data/datasets/pisa/pisa-2025-datasets/questionnaires/STUDENT%20QUESTIONNAIRE%20PISA%202025.pdf', 'status': 'downloaded', 'bytes': 1638887}, {'file': 'volume1_chapter4.html', 'url': 'https://www.oecd.org/en/publications/pisa-2025-results-volume-i_73451bc5-en/full-report/student-school-life-and-beyond_861e5904.html', 'status': 'HTTP Error 403: Forbidden'}, {'file': 'research_documentation.html', 'url': 'https://www.oecd.org/en/about/programmes/pisa/how-to-prepare-and-analyse-the-pisa-database.html', 'status': 'HTTP Error 403: Forbidden'}]
- Decisión: Fuentes oficiales archivadas para auditoría
- Problemas: Ninguno

## 2026-10-06T09:49:49.711786-05:00
- Análisis: Inspección ZIP y espacio libre
- Resultado: [('STU', 992910196), ('SCH', 5416400), ('LDW', 93184353)]
- Decisión: Originales conservados; SPSS extraídos solo a work/raw; ZIP sin duplicar.
- Problemas: Ninguno

## 2026-10-06T11:55:40.744763-05:00
- Análisis: Metadatos LDW
- Resultado: 721037 filas; 225 variables
- Decisión: Lectura metadataonly; no observaciones cargadas
- Problemas: Ninguno

## 2026-10-06T11:55:40.902377-05:00
- Análisis: Metadatos SCH
- Resultado: 25133 filas; 458 variables
- Decisión: Lectura metadataonly; no observaciones cargadas
- Problemas: Ninguno

## 2026-10-06T11:55:41.285192-05:00
- Análisis: Metadatos STU
- Resultado: 755721 filas; 885 variables
- Decisión: Lectura metadataonly; no observaciones cargadas
- Problemas: Ninguno

## 2026-10-06T12:59:28.871234-05:00
- Análisis: Contraste SPSS con codebook oficial
- Resultado: 873/885 coincidencias exactas de etiquetas y categorías
- Decisión: Discrepancias conservadas; no inferir códigos; cobertura observada separada de administración
- Problemas: Ninguno

## 2026-10-06T12:59:35.748230-05:00
- Análisis: Dataset reducido y auditoría missing
- Resultado: 755721 filas, 154 columnas, 90 países/economías
- Decisión: Conservar todos los estudiantes; convertir solo códigos especiales documentados; sin imputación y sin filtrar países aún
- Problemas: Ninguno

## 2026-10-06T13:02:59.142772-05:00
- Análisis: Contraste SPSS con codebook oficial
- Resultado: 873/885 coincidencias exactas de etiquetas y categorías
- Decisión: Discrepancias conservadas; no inferir códigos; cobertura observada separada de administración
- Problemas: Ninguno

## 2026-10-06T13:03:06.060738-05:00
- Análisis: Validación de distribuciones contra compendio OCDE
- Resultado: {'point_estimate_checks': 1800, 'passed': 1680, 'max_abs_difference_pp': np.float64(0.004996505052300648), 'status': 'POINT_ESTIMATES_FAIL', 'inference_gate': 'CLOSED: explicit 2025 Fay factor and SE/performance validation pending'}
- Decisión: Denominador oficial incluye no respuesta; publicar solo auditoría de puntos, sin inferencia
- Problemas: Factor Fay 2025 y validación de SE/media de rendimiento pendientes

## 2026-10-06T13:05:03.473843-05:00
- Análisis: Validación de distribuciones contra compendio OCDE
- Resultado: {'point_estimate_checks': 1680, 'passed': 1680, 'max_abs_difference_pp': np.float64(0.004996505052300648), 'status': 'POINT_ESTIMATES_PASS', 'unavailable_country_variable_pairs': 24, 'inference_gate': 'CLOSED: explicit 2025 Fay factor and SE/performance validation pending'}
- Decisión: Denominador oficial incluye no respuesta; publicar solo auditoría de puntos, sin inferencia
- Problemas: Factor Fay 2025 y validación de SE/media de rendimiento pendientes

## 2026-10-06T13:05:50.026879-05:00
- Análisis: Inspección ZIP y espacio libre
- Resultado: [('STU', 992910196), ('SCH', 5416400), ('LDW', 93184353)]
- Decisión: Originales conservados; SPSS extraídos solo a work/raw; ZIP sin duplicar.
- Problemas: Ninguno

## 2026-10-06T13:05:51.317484-05:00
- Análisis: Documentación OCDE descargada
- Resultado: [{'file': 'database.html', 'url': 'https://www.oecd.org/en/data/datasets/pisa-2025-database.html', 'status': 'HTTP Error 403: Forbidden'}, {'file': 'codebook.xlsx', 'url': 'https://webfs.oecd.org/pisa2022/2025/PISA2025_Codebook.xlsx', 'status': 'downloaded', 'bytes': 985161}, {'file': 'technical_report.zip', 'url': 'https://www.oecd.org/content/dam/oecd/en/about/programmes/edu/pisa/publications/technical-report/PISA%202025%20Technical%20Report.zip', 'status': 'HTTP Error 403: Forbidden'}, {'file': 'student_questionnaire.pdf', 'url': 'https://www.oecd.org/content/dam/oecd/en/data/datasets/pisa/pisa-2025-datasets/questionnaires/STUDENT%20QUESTIONNAIRE%20PISA%202025.pdf', 'status': 'downloaded', 'bytes': 1638887}, {'file': 'volume1_chapter4.html', 'url': 'https://www.oecd.org/en/publications/pisa-2025-results-volume-i_73451bc5-en/full-report/student-school-life-and-beyond_861e5904.html', 'status': 'HTTP Error 403: Forbidden'}, {'file': 'research_documentation.html', 'url': 'https://www.oecd.org/en/about/programmes/pisa/how-to-prepare-and-analyse-the-pisa-database.html', 'status': 'HTTP Error 403: Forbidden'}, {'file': 'questionnaire_compendia.zip', 'url': 'https://webfs.oecd.org/pisa2022/2025/Compendia_PISA2025_QQQ.zip', 'status': 'downloaded', 'bytes': 53856097}, {'file': 'official_recoding.zip', 'url': 'https://webfs.oecd.org/pisa2022/2025/PISA_recoding_2025.zip', 'status': 'downloaded', 'bytes': 49239}, {'file': 'student_questionnaire_pba.pdf', 'url': 'https://www.oecd.org/content/dam/oecd/en/data/datasets/pisa/pisa-2025-datasets/questionnaires/PAPER-BASED%20STUDENT%20QUESTIONNAIRE%20PISA%202025.pdf', 'status': 'downloaded', 'bytes': 1563480}, {'file': 'student_questionnaire_uh.pdf', 'url': 'https://www.oecd.org/content/dam/oecd/en/data/datasets/pisa/pisa-2025-datasets/questionnaires/STUDENT%20UNE%20HEURE%20(UH)%20QUESTIONNAIRE%20PISA%202025.pdf', 'status': 'downloaded', 'bytes': 891558}]
- Decisión: Fuentes oficiales archivadas para auditoría
- Problemas: Ninguno

## 2026-10-06T13:06:03.198129-05:00
- Análisis: Dataset reducido y auditoría missing
- Resultado: 755721 filas, 154 columnas, 90 países/economías
- Decisión: Conservar todos los estudiantes; convertir solo códigos especiales documentados; sin imputación y sin filtrar países aún
- Problemas: Ninguno

## 2026-10-06T13:07:48.375921-05:00
- Análisis: Administración: cuestionarios maestros CBA/PBA/UH
- Resultado: [{'file': 'student_questionnaire.pdf', 'pages': 82, 'term_pages_1_based': {'ST438': [61], 'ST436Q16DA': [59], 'ST430': [6], 'Artificial Intelligence': [59, 61]}}, {'file': 'student_questionnaire_pba.pdf', 'pages': 63, 'term_pages_1_based': {'ST438': [], 'ST436Q16DA': [], 'ST430': [5], 'Artificial Intelligence': []}}, {'file': 'student_questionnaire_uh.pdf', 'pages': 32, 'term_pages_1_based': {'ST438': [], 'ST436Q16DA': [], 'ST430': [5], 'Artificial Intelligence': []}}]
- Decisión: Presencia documental de ítems por versión; no asumir selección individual ni sustituir documentación técnica
- Problemas: Ninguno

## 2026-10-06T13:08:53.836516-05:00
- Análisis: Contraste SPSS con codebook oficial
- Resultado: 873/885 coincidencias exactas de etiquetas y categorías
- Decisión: Discrepancias conservadas; no inferir códigos; cobertura observada separada de administración
- Problemas: Ninguno

## 2026-10-06T13:08:57.993045-05:00
- Análisis: Informe de etapas 1–2
- Resultado: Diccionario, reducido y 1680 validaciones puntuales disponibles
- Decisión: Detener inferencia hasta cerrar documentación de varianza/administración; no producir resultados de hipótesis no estimadas
- Problemas: Ninguno

## 2026-10-06T13:09:51.754627-05:00
- Análisis: Control de calidad final de preparación
- Resultado: {'stage1_data_checks': 'PASS', 'rows': 755721, 'columns': 154, 'country_count': 90, 'OECD_country_count': 38, 'keys': 'CNT+CNTSTUID unique', 'valid_AI_categories': '1-5 only plus null', 'valid_critical_practice_categories': '1-4 only plus null', 'replicate_weights': '80, finite, nonnegative', 'official_point_validation': 'POINT_ESTIMATES_PASS', 'inference_status': 'NOT_EXECUTED; see METHODOLOGICAL_BLOCKERS.md'}
- Decisión: Diccionario, tipos/categorías, llaves, pesos y archivos comprobados; inferencia no ejecutada
- Problemas: Ninguno

## 2026-10-06T13:47:55.122656-05:00
- Análisis: Fuentes oficiales adicionales ETAPA 2A
- Resultado: [{'file': 'technical_standards_2025.pdf', 'url': 'https://www.oecd.org/content/dam/oecd/en/about/programmes/edu/pisa/publications/technical-standards/PISA_2025_Technical_Standards.pdf', 'status': 'downloaded', 'bytes': 711775}, {'file': 'integrated_design_2025.pdf', 'url': 'https://www.oecd.org/content/dam/oecd/en/about/programmes/edu/pisa/pisa-database/survey-implementation-tools/pisa-2025/PISA-2025-Integrated-Design.pdf', 'status': 'downloaded', 'bytes': 3552005}, {'file': 'npm_manual_part2_2025.pdf', 'url': 'https://www.oecd.org/content/dam/oecd/en/about/programmes/edu/pisa/pisa-database/survey-implementation-tools/pisa-2025/PISA-2025-National-Project-Manager-NPM-Manual-Part-2.pdf', 'status': 'downloaded', 'bytes': 1545728}, {'file': 'technical_report.zip', 'url': 'https://www.oecd.org/content/dam/oecd/en/about/programmes/edu/pisa/publications/technical-report/PISA%202025%20Technical%20Report.zip', 'status': 'HTTP Error 403: Forbidden'}]
- Decisión: Registrar contenido realmente accesible; no sustituir factor Fay con el de otros ciclos
- Problemas: Ninguno

## 2026-10-06T13:48:39.607325-05:00
- Análisis: Extracción selectiva ETAPA 2A y SENWT
- Resultado: Archivo de auditoría (755721, 46); reducido (755721, 156)
- Decisión: Conservar códigos crudos solo en archivo de auditoría; añadir SENWT y Option_UH al reducido con llaves verificadas
- Problemas: Ninguno

## 2026-10-06T13:53:39.257169-05:00
- Análisis: ETAPA 2A: cobertura, modalidades y contrastes descriptivos 10 PV
- Resultado: {'rows': 755721, 'countries': 90, 'OECD_countries': 38, 'SENWT_all_formula_pass': True, 'SENWT_all_sum_pass': True, 'SENWT_max_relative_difference': np.float64(4.5185789667353684e-14), 'classification_counts': {'CBA_standard': 714959, 'PBA': 34684, 'UH': 5119, 'CBA_UO_labelled': 958, 'unresolved_form': 1}, 'ST438_status_counts': {'administered_evidence': 703962, 'not_administered': 50420, 'unknown': 1339}, 'OECD_failures_by_variable': {'AIUSESCH': ['ISR', 'USA'], 'ST436Q16DA': ['CAN', 'CHL', 'CRI', 'FRA', 'ISR', 'USA'], 'ST438Q01DA': ['ISR', 'USA'], 'ST438Q02DA': ['ISR', 'USA'], 'ST438Q03DA': ['ISR', 'USA'], 'ST438Q04DA': ['ISR', 'USA']}, 'all_failures_by_variable': {'AIUSESCH': ['ARG', 'ARM', 'BGR', 'ISR', 'KHM', 'KSV', 'LBN', 'MKD', 'MUS', 'PRY', 'QKI', 'QTJ', 'RWA', 'URY', 'USA', 'ZMB'], 'ST436Q16DA': ['ARG', 'ARM', 'AZE', 'BGR', 'BRA', 'CAN', 'CHL', 'CRI', 'DOM', 'FRA', 'GEO', 'GTM', 'ISR', 'JOR', 'KEN', 'KGZ', 'KHM', 'KSV', 'LBN', 'MAR', 'MKD', 'MLT', 'MNE', 'MUS', 'PER', 'PRY', 'PSE', 'QAT', 'QKI', 'QTJ', 'RWA', 'SAU', 'SLV', 'SRB', 'URY', 'USA', 'ZMB'], 'ST438Q01DA': ['ARG', 'ARM', 'BGR', 'ISR', 'KHM', 'KSV', 'LBN', 'MUS', 'PRY', 'QKI', 'QTJ', 'RWA', 'URY', 'USA', 'ZMB'], 'ST438Q02DA': ['ARG', 'ARM', 'BGR', 'ISR', 'KHM', 'KSV', 'LBN', 'MKD', 'MUS', 'PRY', 'QKI', 'QTJ', 'RWA', 'URY', 'USA', 'ZMB'], 'ST438Q03DA': ['ARG', 'ARM', 'BGR', 'GTM', 'ISR', 'KHM', 'KSV', 'LBN', 'MKD', 'MUS', 'PRY', 'QKI', 'QTJ', 'RWA', 'URY', 'USA', 'ZMB'], 'ST438Q04DA': ['ARG', 'ARM', 'BGR', 'GTM', 'ISR', 'KHM', 'KSV', 'LBN', 'MKD', 'MUS', 'PRY', 'QKI', 'QTJ', 'RWA', 'URY', 'USA', 'ZMB']}, 'unexpected_codes_total': 0, 'regressions_executed': False, 'Fay_numeric_2025_confirmed': False}
- Decisión: Publicar todos los países y flags del 75%; mantener M1–M5 sin ejecutar
- Problemas: Constante numérica Fay 2025 no confirmada; contrastes sin SE

## 2026-10-06T13:55:54.553253-05:00
- Análisis: Validación de distribuciones contra compendio OCDE
- Resultado: {'point_estimate_checks': 1680, 'passed': 1680, 'max_abs_difference_pp': np.float64(0.004996505052300648), 'status': 'POINT_ESTIMATES_PASS', 'unavailable_country_variable_pairs': 24, 'inference_gate': 'CLOSED: explicit 2025 Fay factor and SE/performance validation pending'}
- Decisión: Denominador oficial incluye no respuesta; publicar solo auditoría de puntos, sin inferencia
- Problemas: Factor Fay 2025 y validación de SE/media de rendimiento pendientes

## 2026-10-06T13:56:04.064952-05:00
- Análisis: ETAPA 2A: cobertura, modalidades y contrastes descriptivos 10 PV
- Resultado: {'rows': 755721, 'countries': 90, 'OECD_countries': 38, 'SENWT_all_formula_pass': True, 'SENWT_all_sum_pass': True, 'SENWT_max_relative_difference': np.float64(4.5185789667353684e-14), 'classification_counts': {'CBA_standard': 714959, 'PBA': 34684, 'UH': 5119, 'CBA_UO_labelled': 958, 'unresolved_form': 1}, 'ST438_status_counts': {'administered_evidence': 703962, 'not_administered': 50420, 'unknown': 1339}, 'OECD_failures_by_variable': {'AIUSESCH': ['ISR', 'USA'], 'ST436Q16DA': ['CAN', 'CHL', 'CRI', 'FRA', 'ISR', 'USA'], 'ST438Q01DA': ['ISR', 'USA'], 'ST438Q02DA': ['ISR', 'USA'], 'ST438Q03DA': ['ISR', 'USA'], 'ST438Q04DA': ['ISR', 'USA']}, 'all_failures_by_variable': {'AIUSESCH': ['ARG', 'ARM', 'BGR', 'ISR', 'KHM', 'KSV', 'LBN', 'MKD', 'MUS', 'PRY', 'QKI', 'QTJ', 'RWA', 'URY', 'USA', 'ZMB'], 'ST436Q16DA': ['ARG', 'ARM', 'AZE', 'BGR', 'BRA', 'CAN', 'CHL', 'CRI', 'DOM', 'FRA', 'GEO', 'GTM', 'ISR', 'JOR', 'KEN', 'KGZ', 'KHM', 'KSV', 'LBN', 'MAR', 'MKD', 'MLT', 'MNE', 'MUS', 'PER', 'PRY', 'PSE', 'QAT', 'QKI', 'QTJ', 'RWA', 'SAU', 'SLV', 'SRB', 'URY', 'USA', 'ZMB'], 'ST438Q01DA': ['ARG', 'ARM', 'BGR', 'ISR', 'KHM', 'KSV', 'LBN', 'MUS', 'PRY', 'QKI', 'QTJ', 'RWA', 'URY', 'USA', 'ZMB'], 'ST438Q02DA': ['ARG', 'ARM', 'BGR', 'ISR', 'KHM', 'KSV', 'LBN', 'MKD', 'MUS', 'PRY', 'QKI', 'QTJ', 'RWA', 'URY', 'USA', 'ZMB'], 'ST438Q03DA': ['ARG', 'ARM', 'BGR', 'GTM', 'ISR', 'KHM', 'KSV', 'LBN', 'MKD', 'MUS', 'PRY', 'QKI', 'QTJ', 'RWA', 'URY', 'USA', 'ZMB'], 'ST438Q04DA': ['ARG', 'ARM', 'BGR', 'GTM', 'ISR', 'KHM', 'KSV', 'LBN', 'MKD', 'MUS', 'PRY', 'QKI', 'QTJ', 'RWA', 'URY', 'USA', 'ZMB']}, 'unexpected_codes_total': 0, 'regressions_executed': False, 'Fay_numeric_2025_confirmed': False}
- Decisión: Publicar todos los países y flags del 75%; mantener M1–M5 sin ejecutar
- Problemas: Constante numérica Fay 2025 no confirmada; contrastes sin SE

## 2026-10-06T14:00:18.545355-05:00
- Análisis: Informe ETAPA 2A y decisión
- Resultado: STOP
- Decisión: STOP: reformular estimando y resolver método antes de modelos
- Problemas: Fay 2025 y dominios de administración pendientes; no cobertura sistemática estadounidense documentada

## 2026-10-06T14:01:30.309027-05:00
- Análisis: Reconciliación independiente ETAPA 2A
- Resultado: {'data_checks': 'PASS', 'audit_decision': 'STOP', 'coverage_rows': 540, 'student_rows': 755721, 'subset_columns': 156, 'countries': 90, 'OECD_countries': 38, 'official_ST438_checks': 1680, 'official_example_checks': 2, 'coverage_partitions_reconcile': True, 'PV_partition_means_reconcile': True, 'SENWT_formula_pass': True, 'CBA_PBA_within_country_contrasts': 'not identifiable; all NA', 'inference': 'NOT_EXECUTED', 'sha256': {'results/selection_audit.md': '62faeb590a78895303620b531f1c1c59001f8a4f140f3803ba4a1fe3de9a6a39', '../../results/aggregated/ai_coverage_by_country.csv': 'f0f0fc36c712109c1b57df08a3f3407ff7c399354eb4505d5facc592bbbdd7b5', '../../results/validation/selection_official_reproduction.csv': '1803fccfca1aed5614756d2b441f0adc5a50d82cf7db53cac570933f9babd53d', '../../results/aggregated/selection_performance_by_country.csv': '5630e730ecd12ef0272fc3510a5284723123fcc243da38c94545f2c2beb27e28'}}
- Decisión: Comprobaciones de datos PASS; decisión científica STOP sin ejecutar modelos
- Problemas: Ninguno

## 2026-10-06T14:03:54.842698-05:00
- Análisis: Informe ETAPA 2A y decisión
- Resultado: STOP
- Decisión: STOP: reformular estimando y resolver método antes de modelos
- Problemas: Fay 2025 y dominios de administración pendientes; no cobertura sistemática estadounidense documentada

## 2026-10-06T14:03:58.944139-05:00
- Análisis: Reconciliación independiente ETAPA 2A
- Resultado: {'data_checks': 'PASS', 'audit_decision': 'STOP', 'coverage_rows': 540, 'student_rows': 755721, 'subset_columns': 156, 'countries': 90, 'OECD_countries': 38, 'official_ST438_checks': 1680, 'official_example_checks': 2, 'coverage_partitions_reconcile': True, 'PV_partition_means_reconcile': True, 'SENWT_formula_pass': True, 'CBA_PBA_within_country_contrasts': 'not identifiable; all NA', 'inference': 'NOT_EXECUTED', 'sha256': {'results/selection_audit.md': 'ec733ec522eaea9146245c69e061f4bd14b5370e85be8043a19ebd88468e86b9', '../../results/aggregated/ai_coverage_by_country.csv': 'f0f0fc36c712109c1b57df08a3f3407ff7c399354eb4505d5facc592bbbdd7b5', '../../results/validation/selection_official_reproduction.csv': '1803fccfca1aed5614756d2b441f0adc5a50d82cf7db53cac570933f9babd53d', '../../results/aggregated/selection_performance_by_country.csv': '5630e730ecd12ef0272fc3510a5284723123fcc243da38c94545f2c2beb27e28'}}
- Decisión: Comprobaciones de datos PASS; decisión científica STOP sin ejecutar modelos
- Problemas: Ninguno

## 2026-10-06T14:32:52.627535-05:00
- Análisis: Autorización ETAPA 2B
- Resultado: PASS WITH RESTRICTED ESTIMAND provisional
- Decisión: Validar k=0.5 empíricamente antes de M0/M1/M2; no mantener STOP global
- Problemas: Ninguno

## 2026-10-06T14:33:24.595696-05:00
- Análisis: Tablas oficiales para validar Fay 2025
- Resultado: <research-workspace>\outputs\data\documentation\pisa2025_annex_b1_2a.xlsx
- Decisión: Extraer medias y SE de I.B1.2a.1–3 sin inferir números desde gráficas
- Problemas: Ninguno

## 2026-10-06T14:34:30.755055-05:00
- Análisis: Validación empírica de medias y SE 2025
- Resultado: {'status': 'PASS', 'message': 'FAY VALIDATION PASS — k=0.5 empirically reproduces published PISA 2025 SEs', 'checks': 18, 'passed': 18, 'criterion': 'same display rounding as official workbook cells, before any regression', 'max_abs_mean_diff': np.float64(4.894058974969084e-06), 'max_abs_SE_diff': np.float64(4.49443314565201e-06), 'k': 0.5, 'R': 80, 'M': 10, 'source': 'OECD I.B1.2a.1–3, StatLink mrq53f'}
- Decisión: Continuar M0/M1/M2 automáticamente
- Problemas: Ninguno

## 2026-10-06T14:40:05.506635-05:00
- Análisis: Modelos nacionales M0,M1
- Resultado: 36 candidatos principales; 32 candidatos H6; 64.8s
- Decisión: Media OCDE posterior solo con países que pasan cobertura conjunta; ISR/USA apéndice; conservar no estimables
- Problemas: Ninguno

## 2026-10-06T14:41:28.181154-05:00
- Análisis: Modelos nacionales M2
- Resultado: 36 candidatos principales; 32 candidatos H6; 37.7s
- Decisión: Media OCDE posterior solo con países que pasan cobertura conjunta; ISR/USA apéndice; conservar no estimables
- Problemas: Ninguno

## 2026-10-06T14:42:34.544709-05:00
- Análisis: Síntesis igualitaria y sensibilidades M2
- Resultado: 60 contrastes principales, siete escenarios y nueve pruebas secundarias de patrones
- Decisión: Combinar varianzas nacionales independientes; no incluir ISR/USA; no ajustar M3/M4/M5
- Problemas: Ninguno

## 2026-10-06T14:44:38.374876-05:00
- Análisis: Figuras de lectura M2
- Resultado: Forest nacional y perfiles categóricos
- Decisión: Mostrar IC del diseño y referencia, sin curvas causales ni PV individuales promediados
- Problemas: Ninguno

## 2026-10-06T14:45:57.339397-05:00
- Análisis: Control independiente ETAPA 2B
- Resultado: {'data_and_numerical_checks': 'PASS', 'Fay_checks': 18, 'independent_SVD_WLS_checks': 9, 'max_SVD_coefficient_difference': 1.8332002582610585e-12, 'primary_FDR_family_size': 60, 'models_fitted': ['M1', 'M2'], 'M0_descriptives': True, 'M3_M4_M5_LDW_fitted': False, 'candidate_ST438_K': 36, 'candidate_H6_K': 32, 'primary_M2_K': [21], 'no_complete_case_country_codes': ['AUS', 'BEL', 'CAN', 'CHL', 'COL', 'CRI', 'DEU', 'DNK', 'ESP', 'IRL', 'ISL', 'LUX', 'NLD', 'NOR', 'NZL'], 'SHA256': {'fay2025_validation.csv': 'dd85f491d6366ad7a4c5e777d23a77f05613cd4cc14101301604693ff8a35934', 'model_joint_coverage.csv': 'dadb854cf513a96221c77cb69ad68c5a960bec09a0060ac6ba427864f9cf0b09', 'descriptives_M0.csv': '8d7a62ecb6e475e3aec5c07edf5be96f33099fb843dcdbe8975f3e8fd1982718', 'country_effects_M1.csv': 'cee167ed338ce9b4d1e1e07a3c328a77163e14725a4329672607e0134294a949', 'country_effects_M2.csv': '2090c910e4cf82d43c46dbf3d7daa91fc35e1d0a177d93ce5e4be88d85b6590a', 'oecd_equal_weight_summary_M2.csv': '793a791713552eadf30e294cdaa017aac7cccccd0d4e1b2afce63694a88f1977', 'primary_contrasts_M2.csv': '793a791713552eadf30e294cdaa017aac7cccccd0d4e1b2afce63694a88f1977', 'selection_sensitivity.csv': 'a9425bb543f3580601f5f1c5646baf93f79b37b2dd6b08809e23dfee0a57540b', 'low_coverage_exploratory_ISR_USA.csv': '03eab14756fec780aacce8c70a2e7413d8bb6e134fd5d3cdfffc12c6c6deb0c0'}}
- Decisión: Datos/varianza/SVD/FDR y exclusiones conciliados; solo M0/M1/M2
- Problemas: Ninguno

## 2026-10-06T14:47:16.542746-05:00
- Análisis: Síntesis igualitaria y sensibilidades M2
- Resultado: 60 contrastes principales, siete escenarios y nueve pruebas secundarias de patrones
- Decisión: Combinar varianzas nacionales independientes; no incluir ISR/USA; no ajustar M3/M4/M5
- Problemas: Ninguno

## 2026-10-06T14:50:24.502397-05:00
- Análisis: Informe ETAPA 2B completo
- Resultado: {'status': 'PASS WITH RESTRICTED ESTIMAND', 'Fay_validation': 'FAY VALIDATION PASS — k=0.5 empirically reproduces published PISA 2025 SEs', 'M0_M1_M2': 'COMPLETE; strict M2 with unavailable-country rows preserved', 'M3_M4_M5_LDW': 'NOT EXECUTED', 'main_ST438_candidate_K': 36, 'main_M2_K': 21, 'H6_candidate_K': 32, 'user_M2_missing_covariate_decision': 'keep complete M2; mark non-estimable countries', 'quality_checks': 'PASS', 'H1_H2_H3_H4': 'supported only for stated restricted M2 estimand', 'H5': 'mixed'}
- Decisión: Mantener estimando restringido; presentar pérdida de países y sensibilidad de aprender; revisar M2 antes de modelos adicionales
- Problemas: Ninguno

## 2026-10-06T14:51:51.724088-05:00
- Análisis: Cierre de entregables ETAPA 2B
- Resultado: {'bundle': 'STAGE_2B_DELIVERABLES.zip', 'bytes': 1043081, 'SHA256': 'a5281eb67950764b5c724266b9c2b2dcdd2ed95823e31312f2740273bc71d3db', 'members': ['../../results/validation/fay2025_validation.csv', '../../results/aggregated/model_joint_coverage.csv', '../../results/aggregated/descriptives_M0.csv', '../../results/aggregated/country_effects_M1.csv', '../../results/aggregated/country_effects_M2.csv', '../../results/aggregated/oecd_equal_weight_summary_M2.csv', '../../results/aggregated/primary_contrasts_M2.csv', '../../results/robustness/selection_sensitivity.csv', '../../results/aggregated/low_coverage_exploratory_ISR_USA.csv', 'figures/forest_reading_summary.png', 'figures/ai_frequency_reading.png', 'STAGE_2B_REPORT.md', 'STAGE_2B_PLAN.md', 'requirements.txt', 'sources.md', '../../results/robustness/secondary_REML_M2.csv', '../../results/robustness/learn_vs_other_pattern_tests_M2.csv', '../../results/robustness/learn_vs_other_pattern_sensitivity_M2.csv', '../../results/robustness/learn_vs_other_level_differences_M2.csv', '../../results/aggregated/stage2b_covariate_availability.csv', '../../results/aggregated/stage2b_country_eligibility.csv', 'results/stage2b_status.json', 'results/stage2b_quality_checks.json', '../../results/aggregated/national_fit_diagnostics.csv', 'results/fay2025_validation_status.json', '../../results/validation/fay2025_validation_by_pv.csv', '../../results/validation/independent_WLS_checks.csv', '../../results/aggregated/M1_M2_country_set_comparison.csv', '../../results/aggregated/une_heure_oecd.csv', 'scripts/common.py', 'scripts/2b_check_results.py', 'scripts/2b_download_official.py', 'scripts/2b_figures.py', 'scripts/2b_finalize.py', 'scripts/2b_national_models.py', 'scripts/2b_report.py', 'scripts/2b_status.py', 'scripts/2b_synthesize.py', 'scripts/2b_validate_fay.py'], 'required_deliverables': 12, 'contains_microdata': False}
- Decisión: Entregar informe, tablas y figuras; detener ampliación de modelos para revisión M2
- Problemas: Ninguno

## 2026-10-06T15:44:48.555045-05:00
- Análisis: Preespecificación 2C y disponibilidad
- Resultado: CORE/FE/M3/conjunto/diagnósticos definidos antes de nuevos coeficientes
- Decisión: Separar muestra, países y controles; conservar no estimables
- Problemas: Ninguno

## 2026-10-06T15:49:35.415396-05:00
- Análisis: Diagnósticos 2C
- Resultado: Correlaciones ordinales, celdas, repetición/ausencia y perfiles nacionales
- Decisión: Comparison controls no equivalen a negative controls validados
- Problemas: Ninguno

## 2026-10-06T15:53:47.853057-05:00
- Análisis: Comparadores digitales misma muestra
- Resultado: IA y comportamiento digital ajustados con CORE sobre los mismos estudiantes
- Decisión: No presentar negative controls causales ni combinar diseños internacionales
- Problemas: Ninguno

## 2026-10-06T15:57:26.618190-05:00
- Análisis: Modelos nacionales 2C
- Resultado: CORE/FULL/FE/M3/conjunto y comparadores con 10 PV x 81 pesos
- Decisión: Síntesis posterior solo con cobertura/soporte predefinidos
- Problemas: Ninguno

## 2026-10-06T15:58:53.025217-05:00
- Análisis: Comparadores de tareas digitales
- Resultado: Navegación, compartir tareas y producción; selección por redacción oficial
- Decisión: No asumir exclusión de IA por ausencia de la palabra IA
- Problemas: Ninguno

## 2026-10-06T16:00:57.822423-05:00
- Análisis: Síntesis 2C
- Resultado: Descomposición exacta, cambios emparejados, diferencias de dominios y patrones
- Decisión: Varianzas nacionales independientes, inferencia secundaria y covarianza BRR
- Problemas: Ninguno

## 2026-10-06T16:07:26.753963-05:00
- Análisis: Informe 2C completo
- Resultado: Hipótesis y respuesta final según criterios predefinidos
- Decisión: Mecanismo indeterminado; no LDW ni artículo final
- Problemas: Ninguno

## 2026-10-06T16:12:20.264039-05:00
- Análisis: Informe 2C completo
- Resultado: Hipótesis y respuesta final según criterios predefinidos
- Decisión: Mecanismo indeterminado; no LDW ni artículo final
- Problemas: Ninguno
