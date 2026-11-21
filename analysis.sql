-- 1) Data quality: identify duplicate transaction IDs
SELECT transaction_id, COUNT(*) AS row_count
FROM transactions
GROUP BY transaction_id
HAVING COUNT(*) > 1;

-- 2) Overall performance and fraud rate
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT transaction_id) AS unique_transactions,
    SUM(is_fraud) AS fraud_transactions,
    ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct
FROM transactions;

-- 3) Fraud rate by payment method
SELECT payment_method,
       COUNT(*) AS transaction_count,
       SUM(is_fraud) AS fraud_count,
       ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct
FROM transactions
GROUP BY payment_method
ORDER BY fraud_rate_pct DESC;

-- 4) High-risk transaction segments
SELECT
    CASE WHEN amount >= 350 THEN 'High value' ELSE 'Standard value' END AS amount_band,
    CASE WHEN transaction_hour BETWEEN 0 AND 4 THEN 'Overnight' ELSE 'Other hours' END AS time_band,
    COUNT(*) AS transaction_count,
    SUM(is_fraud) AS fraud_count,
    ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct
FROM transactions
GROUP BY 1, 2
ORDER BY fraud_rate_pct DESC;

-- 5) Daily fraud monitoring
SELECT transaction_date,
       COUNT(*) AS transaction_count,
       SUM(is_fraud) AS fraud_count,
       ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct,
       ROUND(SUM(CASE WHEN is_fraud=1 THEN amount ELSE 0 END), 2) AS fraud_amount
FROM transactions
GROUP BY transaction_date
ORDER BY transaction_date;

-- 6) Customers with repeated failed attempts and subsequent fraud
SELECT customer_id,
       COUNT(*) AS transactions,
       SUM(failed_attempts_24h) AS failed_attempts,
       SUM(is_fraud) AS fraud_transactions
FROM transactions
GROUP BY customer_id
HAVING SUM(failed_attempts_24h) >= 3
   AND SUM(is_fraud) >= 1
ORDER BY fraud_transactions DESC, failed_attempts DESC;
