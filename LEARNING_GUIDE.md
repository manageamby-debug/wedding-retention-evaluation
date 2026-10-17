# Learn and explain the project

Your backend work is useful: rows, SQL queries, validation and reproducible code carry over. The new part is learning patterns from past examples and measuring whether they work on unseen examples.

## Key ideas

- **Feature:** information available when predicting, such as sessions in the first 14 days.
- **Label:** what you later learn happened: zero sessions during the following 30 days.
- **Logistic regression:** combines weighted features and turns the result into a probability between zero and one. It is a classification model despite its name.
- **Training:** fitting those weights on earlier accounts.
- **Validation:** choosing a decision rule without touching final test outcomes.
- **Testing:** checking the frozen model on later accounts.
- **Leakage:** giving a model an answer or information from the future. Future session count directly reveals our inactivity label, so using it would make the evaluation invalid.
- **Baseline:** a simple reference. Here every user receives the training inactivity rate. A complicated model must earn its complexity by outperforming that reference.
- **Imputation:** replacing missing task counts with the training median. Learning this median from all data would contaminate the training process.

## Reading the numbers

**Precision** asks: of the accounts flagged, how many became inactive? **Recall** asks: of all inactive accounts, how many did we flag? Raising a threshold typically contacts fewer people and changes both. Neither proves outreach works.

**ROC AUC** summarizes ranking across thresholds. Roughly, it is the chance that a randomly chosen inactive account receives a higher score than a randomly chosen active account. A constant model has AUC 0.5.

**Average precision** summarizes precision across recall levels. Its no-skill reference depends on prevalence; use the baseline in the report instead of assuming 0.5.

**Brier score** is mean squared error between predicted probabilities and zero-or-one labels. Lower is better. It is not a substitute for a calibration curve.

**Bootstrap interval:** repeatedly sample test accounts with replacement and recalculate a metric. The interval describes uncertainty under assumptions about those accounts; it does not include all possible real-world uncertainty.

**Association versus causation:** low engagement might predict inactivity. It does not prove increasing sessions or sending messages prevents inactivity. Randomized experiments can help answer the intervention question.

## Hands-on exercises before using this portfolio

1. Run the script and find the model and baseline average precision in metrics.json.
2. Explain why the future-sessions column is excluded.
3. Change the validation quantile from .8 to .9 and rerun. Explain the contact-rate and recall changes; restore .8 afterward.
4. Explain why a 30-day gap separates the periods: prior labels must be observable when the next period begins.
5. Open SQL outputs. Explain why a premium/free difference is not proof that buying premium prevents inactivity.
6. Grade the flawed submission yourself before reading scores.md.

## Interview prompts

**Why this subject?** It connects to my Python/SQL wedding-app backend experience. This separate portfolio experiment uses simulated accounts.

**Did you collect real data?** No. The data generator is included and encodes the relationships. That makes this reproducible, but limits conclusions about real users.

**How did you contribute?** Explain what you actually ran, inspected, changed and learned. Disclose AI assistance. Do not recite work you have not done.

**What would you improve?** Validate on permitted real data, inspect calibration and subgroup performance, define operational costs and test any intervention independently.
