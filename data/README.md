# Datos originales: descarga independiente

Fuente oficial: [PISA 2025 Database](https://www.oecd.org/en/data/datasets/pisa-2025-database.html), apartado **PISA data / Download the datasets**, archivo **Student questionnaire, SPSS**, nombre `CY09_MS_STU_PUF.zip`. Fecha de comprobación del portal: 2026-10-12; análisis original iniciado 2026-10-06.

Sitúe el ZIP en `data/raw/CY09_MS_STU_PUF.zip` o pase `--puf` al controlador. No descomprima con un lector sin Deflate64. El pipeline comprueba SHA-256, tamaño y CRC, y extrae de forma segura únicamente el miembro estudiantil.

- ZIP: 992.910.196 bytes.
- SHA-256: `ef5a76cc20215c09308a541cb3c6ee66583d068ede8535c0b735288e0a71f985`.
- Miembro: `CY09_MS_STU_PUF.sav`, 2.168.666.883 bytes, CRC32 `8ce13fd4`.
- 755.721 filas, 885 variables; revisar cambio de versión si el hash difiere.

El repositorio distribuye código, documentación y resultados agregados; no PUF, SAV, Parquet, datasets estudiantiles reducidos, pesos individuales ni identificadores de estudiantes/escuelas. Los productos locales viven en `.reproduction/` y no son archivos publicables. No subirlos a GitHub/Zenodo.

SCH y LDW se inspeccionaron solo por metadatos durante la preparación: no se requieren para los análisis publicados y no se hace análisis LDW. Las condiciones de uso corresponden a OCDE y deben revisarse en el portal de descarga y [Terms and Conditions](https://www.oecd.org/en/about/terms-conditions.html). La licencia MIT del código no relicencia esos datos. No se afirma que los microdatos tengan una licencia MIT.
