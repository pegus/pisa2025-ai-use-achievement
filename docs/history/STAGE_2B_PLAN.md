> Historical stage document. The current primary model is CORE (32 countries); see ../../README.md.

# Protocolo ETAPA 2B, antes de las regresiones M2

Estimando autorizado: asociación ponderada entre frecuencia declarada de uso de IA y rendimiento PISA entre estudiantes con respuestas válidas a ST438, en sistemas OCDE donde la variable analizada vincula al menos al 75% ponderado de la población objetivo PISA. Se aplica el Technical Standard 6.15; no se estima causalidad ni se generaliza a todos los jóvenes de 15 años.

Estado provisional: PASS WITH RESTRICTED ESTIMAND. La puerta de varianza exige medias y SE oficiales 2025 de AUS/COL/DEU/JPN/MEX/TUR en los tres dominios. k=0.5 es una implementación sometida a comprobación empírica, no una confirmación documental asumida de ciclos anteriores.

M0: frecuencia y medias nacionales por categoría. M1: indicadores de frecuencias 2–5 con referencia 1. M2: los mismos indicadores + ESCS, sexo del marco ST004D01T, AGE, inmigración categórica IMMIG (referencia nativo) y lengua del hogar ST022Q01TA (referencia idioma de la prueba). Sin efectos fijos de país en modelos nacionales. ESCS/AGE se centran en cada muestra nacional para estabilidad numérica; no cambia los contrastes de IA. Covariables constantes se omiten con registro; covariables ausentes no se imputan ni se sustituyen silenciosamente.

M2 completo será la regla por defecto si no se recibe autorización para omitir sexo cuando está ausente nacionalmente. Las muestras sin casos completos conservarán filas no estimables y cobertura 0%, sin un coeficiente inventado. No se sustituye ST004D01T por un género del cuestionario no presente en el PUF.

Países: verificar inicialmente las cuatro coberturas ST438 >=75% (36 previstos; ISR/USA solo apéndice). La síntesis de cada exposición/dominio/modelo exige además cobertura conjunta >=75% en la muestra realmente estimada. Se conservarán todos los resultados nacionales estimables bajo 75%, con flag. H6 solo tendrá diagnóstico de elegibilidad en esta etapa (32 previstos), sin ajustar interacción.

Cobertura prospectiva, sin estimación: M3=M2+ST250Q02JA/ST250Q05JA/ST326Q01JA/02JA/04JA/05JA/ST097Q06DA. M5 candidato=M2+ST436Q16DA para una futura interacción categórica; no incluye covariables escolares todavía no fijadas. Estos flags no certifican la cobertura de una futura especificación escolar distinta. No se ejecutan M3/M4/M5/LDW ni se construye SUBSTITUTIVE_AI_INDEX.

Varianza nacional: 80 réplicas BRR-Fay, factor 1/[80(1−0.5)^2]=1/20. Reestimar cada modelo con diez PV y los 81 juegos de pesos; combinar media de covarianzas muestrales y 1.1 veces covarianza entre PV. Conservar matrices/estimaciones para contrastes correlacionados. No promediar PV individuales como outcome.

Síntesis primaria: media igualitaria de coeficientes nacionales elegibles, con Var(media)=sum(Var nacional)/K² para el conjunto fijo de países. Contrastes principales M2: 48 niveles frente a nunca y 12 diario frente a semanal. Benjamini–Hochberg conjunto sobre exactamente estas 60 pruebas. IC normales de 95%, p bilateral; no errores OLS ordinarios. Nacionales p exploratorios, sin seleccionar países por signo/significancia.

H4: nueve pruebas Wald secundarias de diferencia de los vectores de cuatro contrastes entre aprender y cada otra conducta, para los tres dominios. Usar países elegibles comunes, diferencia de coeficientes obtenidos con las mismas réplicas y PV dentro de país, y sumar covarianzas nacionales independientes. Aplicar BH a estas nueve pruebas separadas de la familia primaria de 60. Las muestras respondientes pueden diferir entre exposiciones; el contraste describe diferencias de asociaciones, no la superioridad causal de una finalidad. H5 exige contrastes mensual/semanal frente a nunca y diario frente a semanal; no se declara una curva por inspección gráfica.

Sensibilidad de selección: A/G todos los países candidatos con cobertura conjunta >=75%; B/C/D >=80/85/90% respectivamente; E además excluir >5% ponderado UH; F además exigir cero registros UH observados. La lista inicial sigue exigiendo >=75% en las cuatro exposiciones. Comparar todas las sensibilidades, incluso con K=0 (NA explícito). A y G son duplicados solicitados y deben coincidir; no se cuentan como evidencia independiente. BH60 se calcula en cada escenario adicional y se etiqueta secundario. Mostrar cambio de conjuntos de países, signo y magnitud.

Heterogeneidad: rango, SD de coeficientes, proporción de signos, Q de Cochran e I² como diagnósticos; no convertir una media significativa en consenso nacional. Meta-análisis REML secundario para los mismos contrastes, sin sustituir la media igualitaria principal.

Interpretación final: supported exige coherencia de signo y magnitud, IC/FDR y robustez entre países/escenarios. mixed cuando cambian patrones, cobertura o dominio; not supported cuando los contrastes no respaldan la afirmación. No escoger un umbral favorable. Colombia permanecerá en M0/M1 y en todas las tablas; su inclusión estimable en M2 completo depende de la disponibilidad real de sexo. ST436Q16DA de Colombia se marca cerca del límite y se muestra su elegibilidad a 80%, sin ejecutar H6.
