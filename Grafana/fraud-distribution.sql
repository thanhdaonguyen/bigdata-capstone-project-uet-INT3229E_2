SELECT
  CASE
    WHEN t.amt < 50 THEN '0 - 50'
    WHEN t.amt >= 50 AND t.amt < 100 THEN '50 - 100'
    WHEN t.amt >= 100 AND t.amt < 200 THEN '100 - 200'
    WHEN t.amt >= 200 AND t.amt < 500 THEN '200 - 500'
    WHEN t.amt >= 500 THEN '500+'
    ELSE 'Unknown'
  END AS amt_range,
  COUNT(*) AS fraud_count_in_range
FROM
  `system-admin-460407.transactions.transactions_input_1` AS t
JOIN
  `system-admin-460407.transactions.spark_fraud_prediction_1` AS f
ON
  t.trans_num = f.trans_id
WHERE
  f.is_fraud = TRUE
GROUP BY
  amt_range
ORDER BY
  amt_range;
