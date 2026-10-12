# Pesos, valores plausibles y BRR-Fay

Dentro de cada país y muestra completa elegible se ajusta Y_m = α + Σ(j=2..5) β_j I(ST438=j) + controles, por mínimos cuadrados ponderados con W_FSTUWT. Se vuelve a estimar con cada W_FSTURWT1–80, para cada m=1..10. No se calcula un rendimiento medio por estudiante.

Para θ_m0 estimación final y θ_mr replicada, k=.5 y R=80:

U_m = Σ_r (θ_mr−θ_m0)(θ_mr−θ_m0)' / [R(1−k)²] = suma /20.

Q̄ = Σ_m θ_m0/10; Ū = Σ_m U_m/10; B = Σ_m(θ_m0−Q̄)(θ_m0−Q̄)'/9; T = Ū + 1.1B.

Contrastes β5−β4 usan toda la covarianza, no suma de SE marginales. CI95 con normal como en la investigación; pruebas BH documentadas por familia. Se publica U/B/T en resultados nacionales.

Validación oficial: AUS/COL/DEU/JPN/MEX/TUR × READ/MATH/SCIE, **18/18** medias y SE reproducidos a precisión editorial, diferencias absolutas <0.000005. [fay2025_validation.csv](../results/validation/fay2025_validation.csv). Fuente oficial: [StatLink mrq53f](https://stat.link/mrq53f), tablas I.B1.2a.1–3. El fixture contiene solo las cifras oficiales, ubicación y formato de celdas; los resultados calculados se vuelven a producir del PUF. El acceso al borrador técnico completo falló en la etapa original: se distingue validación empírica de lectura documental del factor específico. No se adopta .5 meramente por ser un ciclo anterior.

**Síntesis principal:** K países fijos elegibles, Q=ΣQ_c/K y Var(Q)=ΣT_c/K², diseños nacionales independientes. No precisión inversa como estimando principal; REML con Knapp–Hartung modificado es sensibilidad. La suma de estudiantes o pesos de una síntesis describe su muestra, no redefine el promedio como promedio de todos los estudiantes OCDE.

SENWT_c,i = 5000 W_FSTUWT_c,i /Σ_i W_FSTUWT_c,i; suma 5000 por país, constante nacional. Verificado empíricamente; el reescalado nacional no modifica pendientes nacionales. No se estimó un ajuste multinacional con SENWT ni se validó una replicación conjunta independiente de países; esa propuesta permanece sin ejecutar.

**FE escolar:** absorción ponderada recalculada para cada réplica. X y cada Y_PV tienen medias escolares propias en ese peso; nunca reutilizar transformación del peso final. Validación independiente: QR con todas las dummies escolares y experimento sintético de pesos replicados no proporcionales. Escuelas sin variación IA pueden informar covariables pero no identifican directamente su contraste.

**Dominios:** emparejar números PV no confirma por sí solo que los sorteos 2025 sean conjuntos. Se publica covarianza por emparejamiento como sensibilidad; primaria maximiza varianza muestral sobre emparejamientos factibles con asignación mínima de covarianza y usa (sqrt(B_READ)+sqrt(B_other))² como cota de B. Resultado READ−SCIE no robusto en FULL, por lo que no inferir «efecto específico del lenguaje» comparando significancias separadas.
