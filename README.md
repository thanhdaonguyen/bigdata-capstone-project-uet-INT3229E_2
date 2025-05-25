
### 1. **BigQuery**
   - **Purpose**: Contains data files and instructions for setting up BigQuery tables used in the pipeline.
   - **Key Files**:
     - `transactions_input.csv`: Raw transaction data used as input for the pipeline.
     - `fraud_prediction.csv`: Output of the fraud detection model, including predictions and latency information.
     - `README.md`: Detailed guide on how to use the data files and integrate them with BigQuery.
   - **Usage**: Upload these files to BigQuery to create tables for analysis and visualization.

### 2. **Grafana**
   - **Purpose**: Provides resources for visualizing fraud detection metrics using Grafana.
   - **Key Files**:
     - `grafana-bigquery-setup.md`: Step-by-step guide to connect BigQuery to Grafana Cloud.
     - SQL files (`fraud-distribution.sql`, `fraud-ratio.sql`, `latency.sql`, `throughput.sql`, `geographic.sql`): Queries for creating views in Grafana dashboards.
     - `README.md`: Instructions for setting up Grafana and building dashboards.
   - **Usage**: Use the SQL files to create panels in Grafana and visualize fraud detection metrics.

### 3. **Kafka+Flink**
   - **Purpose**: Handles real-time data ingestion and processing using Apache Kafka and Apache Flink.
   - **Key Files**:
     - `producer.py`: Script for producing transaction data to Kafka topics.
     - `flink.py`: Flink job for processing transaction data in real-time.
     - `connect-config-template.json`: Template for configuring Kafka Connect.
     - `README.md`: Instructions for setting up Kafka and Flink for the pipeline.
   - **Usage**: Set up Kafka and Flink to process transaction data in real-time and output results to BigQuery.

#### GitHub Repository
Find the online source code on [Kafka+Flink Github Repo](https://github.com/nvt18624/Bigdata).

### 4. **Spark**
   - **Purpose**: Provides batch processing capabilities for analyzing large datasets.
   - **Key Files**:
     - `Dockerfile`: Docker setup for running Spark jobs.
     - Other files: Spark scripts and configurations for batch processing.
   - **Usage**: Use Spark for batch processing tasks, such as aggregating historical data or training models.

#### GitHub Repository
Find the online source code on [Spark Github Repo](https://github.com/png261/spark-kafka-bigquery).


### 5. **Other Files**
   - `presentation.pptx`: Presentation summarizing the project.
   - `report.pdf`: Detailed report on the project.

## How to Use the Pipeline

1. **Set Up BigQuery**:
   - Follow the instructions in `BigQuery/README.md` to create tables in BigQuery.

2. **Set Up Kafka and Flink**:
   - Use the scripts in the `Kafka+Flink` folder to set up Kafka cluster and Flink instances.
   - Refer to `Kafka+Flink/README.md` for detailed instructions.

3. **Set Up Spark**:
   - Use the Spark scripts for batch processing tasks.
   - Refer to the `Spark` folder for configurations and scripts.

4. **Set Up Grafana**:
   - Connect BigQuery to Grafana using the guide in `Grafana/grafana-bigquery-setup.md`.
   - Use the SQL files in the `Grafana` folder to create dashboards.

5. **Visualize and Analyze**:
   - Use Grafana dashboards to monitor fraud detection metrics in real-time.
   - Analyze historical data using BigQuery and Spark.

## Purpose

This project demonstrates a scalable and efficient pipeline for detecting fraudulent transactions. It integrates multiple Big Data tools to handle real-time and batch processing, data storage, and visualization, providing actionable insights into transaction patterns and fraud detection.