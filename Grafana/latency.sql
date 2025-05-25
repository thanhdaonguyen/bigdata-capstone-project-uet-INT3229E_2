
WITH base AS (
  SELECT
    TIMESTAMP_MILLIS(produced_timestamp) AS produced_time,
    latency_ms
  FROM `system-admin-460407.transactions.spark_fraud_prediction_1`
),

-- Get the latest timestamp
max_time AS (
  SELECT MAX(produced_time) AS latest_time FROM base
),

-- Assign each record to a 30s time bucket
binned AS (
  SELECT
    TIMESTAMP_SUB(
      latest_time,
      INTERVAL CAST(FLOOR(TIMESTAMP_DIFF(latest_time, produced_time, SECOND) / 30) AS INT64) * 30 SECOND
    ) AS window_start,
    latency_ms
  FROM base, max_time
  WHERE TIMESTAMP_DIFF(latest_time, produced_time, SECOND) < 300
),

-- Aggregate latency per time bucket
aggregated AS (
  SELECT
    window_start,
    AVG(latency_ms) AS avg_latency_ms
  FROM binned
  GROUP BY window_start
)

SELECT
  window_start,
  avg_latency_ms
FROM aggregated
ORDER BY window_start;
