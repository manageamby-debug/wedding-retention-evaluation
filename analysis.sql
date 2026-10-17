-- Descriptive associations on the whole simulated dataset, not model selection.
SELECT plan, COUNT(*) AS accounts,
       AVG(inactive_next_30d) AS inactivity_rate,
       AVG(sessions_14d) AS mean_sessions
FROM accounts GROUP BY plan;

SELECT CASE WHEN sessions_14d < 4 THEN 'low'
            WHEN sessions_14d < 8 THEN 'medium' ELSE 'high' END AS engagement,
       COUNT(*) AS accounts, AVG(inactive_next_30d) AS inactivity_rate
FROM accounts GROUP BY engagement;

SELECT COUNT(*) AS total_accounts,
       SUM(CASE WHEN tasks_completed_14d IS NULL THEN 1 ELSE 0 END) AS missing_task_counts,
       COUNT(DISTINCT account_id) AS unique_accounts
FROM accounts;
