"""Reproducible synthetic wedding-planner retention benchmark. Python 3.10+."""
from pathlib import Path
import json
import sqlite3
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss, precision_score, recall_score, confusion_matrix, RocCurveDisplay

ROOT = Path(__file__).resolve().parent
for directory in ['data', 'results']:
    (ROOT / directory).mkdir(exist_ok=True)
rng = np.random.default_rng(42)
n = 5000
# Each row represents one distinct account at the end of its first 14 days.
df = pd.DataFrame({
    'account_id': np.arange(1, n + 1),
    'snapshot_day': np.arange(n) // 14,
    'sessions_14d': rng.poisson(6, n),
    'tasks_completed_14d': rng.poisson(4, n),
    'days_since_last_login': rng.integers(0, 15, n),
    'days_until_wedding': rng.integers(60, 541, n),
    'support_tickets_14d': rng.poisson(.6, n),
    'plan': rng.choice(['free', 'premium'], n, p=[.72, .28]),
})
logit = (-.25 - .18 * df.sessions_14d - .16 * df.tasks_completed_14d
         + .18 * df.days_since_last_login + .38 * df.support_tickets_14d
         - .4 * (df.plan == 'premium') + .001 * (df.days_until_wedding - 250))
df['inactive_next_30d'] = rng.binomial(1, 1 / (1 + np.exp(-logit)))
# This column is deliberately forbidden: it is observed AFTER prediction time.
df['future_sessions_30d_LEAKAGE'] = np.where(df.inactive_next_30d == 1, 0, rng.integers(1, 25, n))
df.loc[rng.random(n) < .04, 'tasks_completed_14d'] = np.nan
df.to_csv(ROOT / 'data/accounts.csv', index=False)
with sqlite3.connect(ROOT / 'data/accounts.sqlite') as con:
    df.to_sql('accounts', con, if_exists='replace', index=False)
    sql = (ROOT / 'analysis.sql').read_text()
    for i, statement in enumerate(sql.split(';')):
        if statement.strip():
            pd.read_sql_query(statement, con).to_csv(ROOT / f'results/sql_{i+1}.csv', index=False)

# Train early accounts, validate later accounts, test the latest accounts.
# A 30-day label-maturity gap prevents training on outcomes unavailable at deployment.
train = df[df.snapshot_day < 180]
valid = df[(df.snapshot_day >= 210) & (df.snapshot_day < 250)]
test = df[df.snapshot_day >= 280]
numeric = ['sessions_14d', 'tasks_completed_14d', 'days_since_last_login', 'days_until_wedding', 'support_tickets_14d']
features = numeric + ['plan']
target = 'inactive_next_30d'
preprocess = ColumnTransformer([
    ('numeric', Pipeline([('impute', SimpleImputer(strategy='median')), ('scale', StandardScaler())]), numeric),
    ('category', OneHotEncoder(handle_unknown='ignore'), ['plan'])])
model = Pipeline([('prepare', preprocess), ('model', LogisticRegression(max_iter=1000, random_state=42))])
model.fit(train[features], train[target])
baseline = DummyClassifier(strategy='prior').fit(train[features], train[target])
vp = model.predict_proba(valid[features])[:, 1]
# Capacity policy: contact roughly the highest-risk 20%, chosen before opening test results.
threshold = float(np.quantile(vp, .8))
yp = model.predict_proba(test[features])[:, 1]
bp = baseline.predict_proba(test[features])[:, 1]
y = test[target].to_numpy()
pred = yp >= threshold
boot = np.random.default_rng(123)
aucs, deltas = [], []
for _ in range(1000):
    idx = boot.integers(0, len(y), len(y))
    if len(np.unique(y[idx])) == 2:
        aucs.append(roc_auc_score(y[idx], yp[idx]))
        deltas.append(average_precision_score(y[idx], yp[idx]) - average_precision_score(y[idx], bp[idx]))
metrics = {
    'rows': {'train': len(train), 'validation': len(valid), 'test': len(test)},
    'test_inactivity_rate': float(y.mean()),
    'validation_selected_threshold': threshold,
    'model': {'roc_auc': roc_auc_score(y, yp), 'average_precision': average_precision_score(y, yp), 'brier_score': brier_score_loss(y, yp), 'precision': precision_score(y, pred, zero_division=0), 'recall': recall_score(y, pred), 'contact_rate': float(pred.mean()), 'confusion_matrix_tn_fp_fn_tp': confusion_matrix(y, pred).ravel().tolist()},
    'baseline': {'roc_auc': roc_auc_score(y, bp), 'average_precision': average_precision_score(y, bp), 'brier_score': brier_score_loss(y, bp)},
    'roc_auc_bootstrap_95_percent_interval': np.quantile(aucs, [.025, .975]).tolist(),
    'paired_average_precision_improvement_95_percent_interval': np.quantile(deltas, [.025, .975]).tolist(),
}
(ROOT / 'results/metrics.json').write_text(json.dumps(metrics, indent=2))
pd.DataFrame({'account_id': test.account_id, 'actual_inactive': y, 'risk_probability': yp, 'flagged': pred}).to_csv(ROOT / 'results/test_predictions.csv', index=False)
RocCurveDisplay.from_predictions(y, yp)
plt.title('Synthetic wedding-app inactivity prediction')
plt.tight_layout()
plt.savefig(ROOT / 'results/roc_curve.png', dpi=150)
plt.close()
report = f'''# Technical report: wedding-app inactivity prediction

## Purpose and provenance
This is an AI-assisted personal learning and evaluation project. All 5,000 accounts are simulated; no customer records or professional deployment results are claimed. The simulation deliberately encodes predictable associations. Results demonstrate a workflow, not evidence that real wedding-app behavior follows these relationships.

## Question and prediction time
At day 14 after signup, can we rank accounts by the risk of having zero sessions in the following 30 days? Inactivity is a proxy for disengagement, not contractual cancellation. Every account is distinct. Weddings are at least 60 days away at the snapshot, limiting the obvious completion-of-event explanation in this simulation.

## Method
Training uses snapshot days below 180; validation uses days 210–249; testing uses days 280 onward. Thirty-day gaps let outcome labels mature before the next period starts. The generator is stationary, so this does not establish robustness to real temporal drift. Account identifiers, dates, labels and future sessions are excluded from predictors. Median imputation, scaling and one-hot encoding are fit within the training pipeline. A logistic regression is compared with a constant training-prevalence baseline. No tuning uses test labels. The validation 80th percentile fixes an approximate 20% outreach policy before test evaluation; the test contact fraction can differ.

## Held-out results
- Rows: training {len(train)}, validation {len(valid)}, test {len(test)}.
- Test inactivity prevalence: {y.mean():.1%}.
- ROC AUC: {metrics['model']['roc_auc']:.3f}; bootstrap 95% interval {metrics['roc_auc_bootstrap_95_percent_interval'][0]:.3f}–{metrics['roc_auc_bootstrap_95_percent_interval'][1]:.3f}.
- Average precision: {metrics['model']['average_precision']:.3f}; baseline {metrics['baseline']['average_precision']:.3f}.
- Brier score (lower is better): {metrics['model']['brier_score']:.3f}; baseline {metrics['baseline']['brier_score']:.3f}.
- At threshold {threshold:.3f}: precision {metrics['model']['precision']:.1%}, recall {metrics['model']['recall']:.1%}, contact rate {metrics['model']['contact_rate']:.1%}.

Intervals use 1,000 account-level resamples of fixed test predictions. They measure sampling uncertainty conditional on this fitted model and simulated population; they exclude retraining variability and simulation misspecification. Brier score measures probability error and alone does not establish calibration. No subgroup fairness or calibration audit has been completed.

## Interpretation and next experiment
The model can rank risk in this simulated environment. It does not show that contacting flagged users causes retention. A real next step would randomize eligible high-risk accounts between outreach and usual care, predefine the 30-day activity outcome, determine sample size from a business-relevant minimum effect, and report an intention-to-treat difference with uncertainty and guardrails. No A/B test was run here.

## Limits
There are no real customer behaviors, realistic acquisition shifts, repeated households, measured intervention costs, or externally validated labels. Missingness is random by construction. Production would require consent and privacy review, real-data validation, monitoring and an explicit cost-benefit decision. The model is an educational benchmark, not a deployment recommendation.
'''
(ROOT / 'results/technical_report.md').write_text(report, encoding='utf-8')
assert set(train.account_id).isdisjoint(test.account_id)
assert train.snapshot_day.max() + 30 < valid.snapshot_day.min()
assert valid.snapshot_day.max() + 30 < test.snapshot_day.min()
assert all('LEAKAGE' not in feature for feature in features)
assert np.isfinite(yp).all() and ((yp >= 0) & (yp <= 1)).all()
print(json.dumps(metrics, indent=2))
print('Integrity checks passed; reports and predictions generated.')
