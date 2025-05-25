# Grafana Setup for Fraud Detection Project

This folder contains the necessary resources to set up Grafana for the Fraud Detection project. It includes SQL files for creating views in the Grafana dashboard and a guide for connecting Google BigQuery to Grafana Cloud.

## Folder Contents

- **[grafana-bigquery-setup.md](grafana-bigquery-setup.md)**: A step-by-step guide to connect Google BigQuery to Grafana Cloud. This includes setting up a Google Cloud project, enabling required APIs, and configuring Grafana Cloud to use BigQuery as a data source.
- **SQL Files**: These files define the queries used to create views in the Grafana dashboard:
  - **[fraud-distribution.sql](fraud-distribution.sql)**: Displays the distribution of fraudulent transactions across different transaction amount ranges.
  - **[fraud-ratio.sql](fraud-ratio.sql)**: Shows the ratio of fraudulent to legitimate transactions.
  - **[latency.sql](latency.sql)**: Calculates the average latency of transactions over time.
  - **[throughput.sql](throughput.sql)**: Measures the throughput of transactions in 30-second intervals.
  - **[geographic.sql](geographic.sql)**: Provides a geographic breakdown of transactions, including fraud rates by city.

## How to Use

1. **Set Up Grafana with BigQuery**:
   - Follow the instructions in [grafana-bigquery-setup.md](grafana-bigquery-setup.md) to configure Grafana Cloud and connect it to your BigQuery dataset.

2. **Create Views in Grafana**:
   - Use the SQL files in this folder to create panels in your Grafana dashboard. Each file corresponds to a specific view:
     - Upload the SQL query to the Grafana query editor for BigQuery.
     - Customize the visualization settings as needed.

3. **Build Dashboards**:
   - Combine the views created from the SQL files into a comprehensive dashboard to monitor fraud detection metrics.

## Purpose

This setup enables real-time monitoring and analysis of fraud detection metrics using Grafana and BigQuery. The SQL queries provide insights into transaction patterns, latency, throughput, and geographic distribution, helping to identify and respond to fraudulent activities effectively.