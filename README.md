# Wedding App Retention: Modeling and Evaluation

An AI-assisted personal portfolio and learning project connecting Python/SQL backend experience with introductory machine learning and evidence-based evaluation. It predicts account inactivity using **entirely synthetic data**, then demonstrates how to grade analytical work.

## Run

Requires Python 3.10 or later. From this folder:

```sh
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run_project.py
```

The seed is fixed. Package versions can affect numerical results; `results/environment.txt` records the environment used for the supplied run. Dependencies in requirements.txt are compatibility ranges, not a cross-platform lockfile.

## Read in this order

1. `LEARNING_GUIDE.md`: concepts and how to explain them.
2. `run_project.py`: simulation, splits, pipeline and metrics.
3. `analysis.sql` and `results/sql_*.csv`: SQL exploration.
4. `results/technical_report.md` and `results/roc_curve.png`: computed findings.
5. `evaluation/rubric.md`, sample submissions and `evaluation/scores.md`: evaluation exercise.

`data/accounts.csv` and `data/accounts.sqlite` contain generated data. `results/test_predictions.csv` makes individual predictions auditable. The deliberately named `future_sessions_30d_LEAKAGE` column must never enter the model. The target is `inactive_next_30d`; all other feature names describe measurements available at the day-14 snapshot. `snapshot_day` is a relative calendar day used only for splitting. One row equals one distinct account.

## Scope

This demonstrates a beginner-to-intermediate workflow, not professional ML experience. No real customer study, deployed product, causal effect or actual AI-system benchmark is claimed. The two sample submissions are authored teaching examples, not outputs collected from an independent model. Evaluation scores are a single illustrative review, not evidence of inter-rater reliability.

Suggested honest portfolio description after studying and rerunning the project:

> Built and studied an AI-assisted personal project on synthetic wedding-app inactivity data using Python and SQL. Implemented a leakage-aware logistic-regression workflow, compared it with a baseline, and used a weighted rubric to review two illustrative analytical submissions.

Do not claim you deployed this model, worked for a client, independently authored every part, or have professional statistics experience from completing it.
