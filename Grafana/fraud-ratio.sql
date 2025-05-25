SELECT
  COUNT(CASE WHEN is_fraud = FALSE THEN 1 END) AS legitimate_count,
  COUNT(CASE WHEN is_fraud = TRUE THEN 1 END) AS fraud_count
FROM
  `system-admin-460407.transactions.spark_fraud_prediction_1`
