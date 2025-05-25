
WITH base AS (
  SELECT
    TIMESTAMP_MILLIS(produced_timestamp) AS produced_time
  FROM `system-admin-460407.transactions.spark_fraud_prediction_1`
),

-- Get the latest time
max_time AS (
  SELECT MAX(produced_time) AS latest_time FROM base
),

-- Assign each transaction to a 30-second bin
binned AS (
  SELECT
    TIMESTAMP_SUB(
      latest_time,
      INTERVAL CAST(FLOOR(TIMESTAMP_DIFF(latest_time, produced_time, SECOND) / 30) AS INT64) * 30 SECOND
    ) AS window_start
  FROM base, max_time
  WHERE TIMESTAMP_DIFF(latest_time, produced_time, SECOND) < 300
),

-- Count transactions per window
throughput_by_window AS (
  SELECT
    window_start,
    COUNT(*) / 30 AS throughput
  FROM binned
  GROUP BY window_start
)

SELECT
  window_start,
  throughput
FROM throughput_by_window
ORDER BY window_start;
