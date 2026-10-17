# Technical report: wedding-app inactivity prediction

## Purpose and provenance
This is an AI-assisted personal learning and evaluation project. All 5,000 accounts are simulated; no customer records or professional deployment results are claimed. The simulation deliberately encodes predictable associations. Results demonstrate a workflow, not evidence that real wedding-app behavior follows these relationships.

## Question and prediction time
At day 14 after signup, can we rank accounts by the risk of having zero sessions in the following 30 days? Inactivity is a proxy for disengagement, not contractual cancellation. Every account is distinct. Weddings are at least 60 days away at the snapshot, limiting the obvious completion-of-event explanation in this simulation.

## Method
Training uses snapshot days below 180; validation uses days 210–249; testing uses days 280 onward. Thirty-day gaps let outcome labels mature before the next period starts. The generator is stationary, so this does not establish robustness to real temporal drift. Account identifiers, dates, labels and future sessions are excluded from predictors. Median imputation, scaling and one-hot encoding are fit within the training pipeline. A logistic regression is compared with a constant training-prevalence baseline. No tuning uses test labels. The validation 80th percentile fixes an approximate 20% outreach policy before test evaluation; the test contact fraction can differ.

## Held-out results
- Rows: training 2520, validation 560, test 1080.
- Test inactivity prevalence: 38.1%.
- ROC AUC: 0.730; bootstrap 95% interval 0.699–0.758.
- Average precision: 0.610; baseline 0.381.
- Brier score (lower is better): 0.201; baseline 0.236.
- At threshold 0.584: precision 63.4%, recall 36.7%, contact rate 22.0%.

Intervals use 1,000 account-level resamples of fixed test predictions. They measure sampling uncertainty conditional on this fitted model and simulated population; they exclude retraining variability and simulation misspecification. Brier score measures probability error and alone does not establish calibration. No subgroup fairness or calibration audit has been completed.

## Interpretation and next experiment
The model can rank risk in this simulated environment. It does not show that contacting flagged users causes retention. A real next step would randomize eligible high-risk accounts between outreach and usual care, predefine the 30-day activity outcome, determine sample size from a business-relevant minimum effect, and report an intention-to-treat difference with uncertainty and guardrails. No A/B test was run here.

## Limits
There are no real customer behaviors, realistic acquisition shifts, repeated households, measured intervention costs, or externally validated labels. Missingness is random by construction. Production would require consent and privacy review, real-data validation, monitoring and an explicit cost-benefit decision. The model is an educational benchmark, not a deployment recommendation.
