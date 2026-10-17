# Evaluation rubric

Score each dimension from 0 to 4, then compute `weight × score / 4`. Sum to 100. Every score requires a specific artifact or quotation and an explanation. Grade the submitted evidence, not presumed intent.

| Dimension | Weight | Full-credit evidence |
|---|---:|---|
| Question, provenance and label | 15 | Prediction time, horizon, population and synthetic origin explicit |
| Data quality and SQL | 15 | Missingness, duplicates, descriptive queries and limitations inspected |
| Leakage and validation | 25 | Future fields excluded, mature labels, disjoint splits, train-only preprocessing |
| Modeling and metrics | 20 | Reproducible baseline and model; ranking, probability and policy metrics |
| Statistical and causal reasoning | 15 | Uncertainty assumptions; no unsupported intervention or causal claim |
| Communication and reproducibility | 10 | Clear limits, runnable code and traceable numbers |

Common anchors: **0** absent or fundamentally invalid; **1** major errors; **2** partly correct with material gaps; **3** mostly correct with specific omissions; **4** complete supporting evidence for this dimension. Reviewers may use integer scores only.

Critical failure flag: target/future leakage or fabricated empirical evidence makes a submission unsuitable regardless of total. Do not silently replace the numerical total with a different score; record the flag separately.

Calibration procedure: two reviewers independently score the same frozen artifact; compare evidence and reconcile differences of more than one point per dimension; retain original and revised scores and reasons. This project describes that process but has not performed a two-reviewer calibration study.
