# Disclosure review

No individual observations, weights or school identifiers are redistributed. School-level diagnostics and all 625-profile / 25-cell joint cross-tabulations are withheld entirely. Raw JSON missingness counts are withheld. If any published row reports a cell with 1â€“9 students, all its numerical statistics/counts/percentages are suppressed together, preserving classification and eligibility flags. This conservative publication policy changes only disclosure, never analytical samples or coefficients. Unredacted outputs are regenerated locally and ignored by Git. National fitted contrasts have >=30 observations per exposure category where support rules apply.

[
  {
    "file": "administration_mode_by_country.csv",
    "rows_suppressed": 1,
    "reason": "1-9 observations in at least one reported cell; entire statistical row withheld"
  },
  {
    "file": "ai_coverage_by_country.csv",
    "rows_suppressed": 224,
    "reason": "1-9 observations in at least one reported cell; entire statistical row withheld"
  },
  {
    "file": "school_FE_support.csv",
    "rows_suppressed": 134,
    "reason": "1-9 observations in at least one reported cell; entire statistical row withheld"
  },
  {
    "file": "selection_candidate_domains.csv",
    "rows_suppressed": 33,
    "reason": "1-9 observations in at least one reported cell; entire statistical row withheld"
  },
  {
    "file": "selection_performance_by_country.csv",
    "rows_suppressed": 138,
    "reason": "1-9 observations in at least one reported cell; entire statistical row withheld"
  },
  {
    "file": "selection_performance_by_pv.csv",
    "rows_suppressed": 1330,
    "reason": "1-9 observations in at least one reported cell; entire statistical row withheld"
  },
  {
    "file": "selection_performance_contrasts.csv",
    "rows_suppressed": 36,
    "reason": "1-9 observations in at least one reported cell; entire statistical row withheld"
  }
]

Complementary protection: per-PV selection-performance partitions are excluded entirely. All grouped performance statistics for a country with any 1–9-student subgroup are withheld, including large/complementary groups, so published partition totals cannot be subtracted to recover a rare subgroup mean. This affects 41 countries in that descriptive table; national model estimates are unchanged.
