# Code adaptations

Statistical kernels are preserved from the staged analyses. Public-only changes are listed here and checked against immutable aggregated reference outputs.

- `2b_validate_fay.py`: Replace extraction from official XLSX with the same 18 extracted official values/cell formats; no arithmetic changes.
- `2c_prepare.py`: Preserve historical plan; generated runtime plan uses a separate file.
- `2c_task_comparators.py`: Replace prior task-comparator rows before append, so repeats do not duplicate results.
- `2c_synthesize.py`: Make same-sample precision merge idempotent; initial-run arithmetic unchanged.
- `common.py`: environment-configurable runtime root; no machine-specific dependency path.
- Pipeline controller: ZIP integrity checks, PUF metadata extraction, ordering, isolated output folders, public/reference checks.
