# Illustrative evidence-based review

One AI-assisted review of two authored teaching examples. Scores are judgments, not independently validated measurements. A is the complete referenced project; B is the short text alone. This artifact asymmetry is intentional and should not be treated as a controlled model comparison.

| Dimension | Weight | A score / 4 | B score / 4 |
|---|---:|---:|---:|
| Question, provenance and label | 15 | 4 | 1 |
| Data quality and SQL | 15 | 3 | 0 |
| Leakage and validation | 25 | 4 | 0 |
| Modeling and metrics | 20 | 3 | 0 |
| Statistical and causal reasoning | 15 | 3 | 0 |
| Communication and reproducibility | 10 | 4 | 1 |
| **Weighted total** | **100** | **87.50** | **6.25** |

## A: evidence and reasons

- Question (4): technical_report.md defines day-14 prediction, next-30-day inactivity, distinct accounts and simulated provenance.
- Quality (3): analysis.sql counts unique accounts and missing task values and groups engagement and plans. The script imputes missingness. Detailed distributions and anomaly investigations are absent.
- Validation (4): run_project.py uses explicit allowed features, train-only pipeline fitting, time gaps and validation-only threshold selection. Integrity checks verify split separation and forbidden feature exclusion.
- Modeling (3): metrics.json includes baseline, ROC AUC, average precision, Brier, precision and recall. A calibration analysis and business utility comparison are absent.
- Reasoning (3): the report describes conditional bootstrap intervals and distinguishes prediction from intervention effects. Experiment sample-size calculation and observed temporal-drift analysis are absent.
- Communication (4): runnable script, requirements, predictions, outputs, learning guide and explicit limitations support traceability.

No critical failure identified within this synthetic educational scope. This score is not a claim of production readiness.

## B: evidence and reasons

- Question (1): “wedding-app customers” provides a subject, but not provenance, prediction time or outcome window.
- Quality (0): “did not need ... SQL checks” and no dataset or quality outputs; full-data imputation also contaminates preprocessing.
- Validation (0): explicitly uses future sessions and selects the cutoff on test results. The future field reveals the outcome directly.
- Modeling (0): unsupported perfect accuracy with no baseline or reproducible predictions cannot establish performance.
- Reasoning (0): “proves ... reduce churn by 30%” has no randomized intervention or other causal identification and no uncertainty.
- Communication (1): readable prose, but no runnable evidence or caveats.

**Critical failure: future leakage and fabricated empirical claims.** Request a rerun excluding future fields, a frozen validation policy, verified outputs, and removal of the causal/deployment claims.
