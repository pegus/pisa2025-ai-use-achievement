# Publication test report

2026-10-12. **REPRODUCIBILITY STATUS: PASS WITH LIMITATIONS.**

Full pipeline completed from the original ZIP (SHA256 and CRC verified), extracting a new SAV and rebuilding the analytical Parquet files in an isolated, ignored directory. No original processed dataset or NPZ estimates were reused. Elapsed: 1379.2 seconds (about 23 minutes). All eight reference comparisons passed: 42,840 national model rows; 720 synthesis rows; 2160 M1 and 2160 M2 rows; 176 domain tests; 60 progression rows; 528 matched digital summaries; 18 official mean/SE validations. Maximum absolute difference in the selected numerical columns across these comparisons: 0.0.

The original independent checks also passed: 18 official Fay mean/SE validations, 1680 ST438 published percentages, 1260 FULL reproduction contrasts, 9 explicit school-dummy QR checks, independent WLS/SVD checks, nonproportional-replicate school-absorption experiment, BH/FDR, coverage/exclusion and country-equal variance reconciliation. Six public unittest checks passed. CITATION.cff was validated with cffconvert against schema 1.2.0. Six PNG figures and the 60-page forest PDF were regenerated.

Limits: tested on Windows/Python 3.12.14 with installed scientific dependencies, not a fresh installation on every platform. CI uses aggregated references and synthetic data, not individual PUF re-estimation. The initial ecological change-score analysis has no available script/table and is not reproduced. SCH/LDW are not analysed. Technical-report access limitations and the restricted estimand remain. Public disclosure suppression differs intentionally from full local descriptive partitions. No causal identification is claimed.

The complete outputs remain local in .reproduction/ and are excluded from Git/Zenodo. Numerical evidence: results/validation/public_reproduction_check.json. Security/disclosure: results/validation/PUBLIC_SECURITY_REVIEW.json and docs/DISCLOSURE_REVIEW.md.
