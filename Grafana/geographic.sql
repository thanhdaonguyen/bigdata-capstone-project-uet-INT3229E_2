
SELECT
  t.city,
  t.lat AS latitude,
  t.long AS longitude,
  COUNTIF(s.is_fraud = TRUE) AS fraud_count,
  COUNT(*) AS total_transactions,
  ROUND(100 * COUNTIF(s.is_fraud = TRUE) / COUNT(*), 2) AS fraud_rate
FROM
  `system-admin-460407.transactions.transactions_input_1` AS t
JOIN 
  `system-admin-460407.transactions.spark_fraud_prediction_1` AS s
ON t.trans_num = s.trans_id
GROUP BY
  t.city, t.lat, t.long
HAVING
  total_transactions > 0  -- lọc bớt thành phố quá ít giao dịch
ORDER BY
  fraud_rate DESC


