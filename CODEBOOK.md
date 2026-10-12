# Variables y reglas de codificación

[VARIABLE_DICTIONARY.csv](docs/VARIABLE_DICTIONARY.csv) conserva códigos, etiquetas oficiales, categorías y rangos SPSS de missing. El pipeline extrae de nuevo metadatos del SAV y aplica solo sus rangos documentados. El diccionario original incluye candidatos inspeccionados; una variable incluida en él no implica que se utilizó en un modelo. La selección final se precisa a continuación y en stage2c_specification.json.

| Código | Uso |
|---|---|
| ST438Q01DA | Resumir lectura asignada |
| ST438Q02DA | Investigación preliminar para trabajos |
| ST438Q03DA | Redactar trabajos escritos |
| ST438Q04DA | Ayudar a aprender |
| AIUSESCH | Índice oficial WLE; auditoría, no sustituto del modelo categórico principal |
| ST436Q16DA | Evaluar información generada por chatbots; auditoría, sin H6/LDW |
| ESCS, IMMIG, ST022Q01TA | Controles CORE |
| ST004D01T, AGE | Controles adicionales FULL, sensibilidad |
| W_FSTUWT, W_FSTURWT1–80 | Peso final y replicados de estudiantes |
| SENWT | Peso senate normalizado a 5000 por país |
| PV1–PV10READ/MATH/SCIE | Diez sorteos por cada dominio, estimación separada |
| ADMINMODE, BOOKID, Option_UH | Auditoría conjunta de administración/modalidades, no exposición |
| CNTSCHID | FE escolar local, nunca redistribuido |
| CNTSTUID | Validación local de unión uno a uno, nunca redistribuido |

ST438 categorías 1–5: nunca/casi nunca, una/dos veces al año, una/dos veces al mes, una/dos veces por semana, diario/casi diario. Referencia 1; cuatro indicadores. Contrastes principales diario–nunca (β5), diario–semanal (β5−β4). No promedio 1–5 como intensidad lineal ni un índice IA inventado.

Missing ST438: 95 valid skip, 96 system missing, 97 not administered, 98 invalid, 99 no response; null separado. ST436 tiene códigos 5–9 equivalentes de missing. Nunca convertir UH/no administrado en «nunca». El denominador de prevalencia oficial ST438 incluye 1–5 y 99, excluye 95–98 y null. El denominador de cobertura es todo el PUF nacional ponderado; son propósitos distintos.

M3 acceso: ST250Q02JA/computadora y ST250Q05JA/internet. M3 potenciales mediadores: ST326Q01JA/Q02JA/Q04JA/Q05JA y ST097Q06DA, con indicadores flexibles. Diagnósticos: ST127Q01TA/02TA/03TA, ST062Q01TA/02TA/03TA, ST001D01T. Comparadores: IC171Q01JA/05JA/06JA; ST322Q07JA; IC176Q02JA/05JA e IC177Q07JA. IC171 categoría 6 es indisponibilidad válida como indicador separado; ST322 categoría 6 no aplicable se excluye. IC177 usa intervalos de horas, no tiene el mismo contraste de frecuencia diaria que ST438.
