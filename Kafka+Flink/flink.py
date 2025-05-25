from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
import json
from google.cloud import bigquery
from google.cloud.exceptions import Conflict
import joblib
import numpy as np
import os
import time


# Configuration
BQ_DATASET = os.environ.get("dataset","default_dataset")
BQ_TABLE = os.environ.get("table", "default_table") 
BQ_PROJECT = os.environ.get("project_id", "default_id") 
BQ_CREDENTIALS_PATH = "/opt/flink/secrets/bq-key.json"
SCHEMA_REGISTRY_URL = "http://" + os.environ.get("zookeeper_ip", "localhost") + ":8081"
KAFKA_TOPIC = os.environ.get("topic_send", "default_topic") 
KAFKA_BOOTSTRAP_SERVERS = os.environ.get("broker1_ip","localhost")  + ":9092"
MODEL_PATH = "/opt/flink/model/model.pkl"


with open(MODEL_PATH, "rb") as f:
    model = joblib.load(f)

# Features required for the model (adjust based on your model's requirements)
FEATURES = [
    "trans_date_trans_time", "cc_num", "merchant", "category", "amt",
    "first", "last", "gender", "street", "city", "state", "zip",
    "lat", "long", "city_pop", "job", "dob", "trans_num", "unix_time",
    "merch_lat", "merch_long"
    ]

def write_to_bigquery(row_json):
    client = bigquery.Client.from_service_account_json(BQ_CREDENTIALS_PATH)
    table_id = f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE}"
    row = json.loads(row_json)
    errors = client.insert_rows_json(table_id, [row])
    if errors:
        print(f"BigQuery errors: {errors}")
    else:
        print("Data successfully inserted into BigQuery.")

# Function to create BigQuery table
def create_bigquery_table():
    client = bigquery.Client.from_service_account_json(BQ_CREDENTIALS_PATH)
    dataset_ref = client.dataset(BQ_DATASET)
    schema_fields = [
        bigquery.SchemaField("trans_id", "INTEGER"),
        bigquery.SchemaField("is_fraud", "BOOLEAN"),
        bigquery.SchemaField("produced_timestamp", "INTEGER"),
        bigquery.SchemaField("processed_timestamp", "INTEGER"),
        bigquery.SchemaField("latency_ms", "INTEGER")
    ]
    table_ref = dataset_ref.table(BQ_TABLE)
    try:
        table = bigquery.Table(table_ref, schema=schema_fields)
        table = client.create_table(table)
        print(f"Table {BQ_TABLE} created successfully.")
    except Conflict:
        print(f"Table {BQ_TABLE} already exists.")

def main():
    # Set up Flink environment
    env = StreamExecutionEnvironment.get_execution_environment()
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    # Add Kafka and Avro dependencies
    t_env.get_config().set("pipeline.jars",
        "file:///opt/flink-1.20.1/lib/flink-connector-kafka-3.4.0-1.20.jar;"
        "file:///opt/flink-1.20.1/lib/kafka-clients-3.7.0.jar;"
        "file:///opt/flink-1.20.1/lib/flink-avro-1.20.1.jar;"
        "file:///opt/flink-1.20.1/lib/flink-avro-confluent-registry-1.20.1.jar;"
        "file:///opt/flink-1.20.1/lib/kafka-schema-registry-client-7.5.0.jar;"
        "file:///opt/flink-1.20.1/lib/kafka-avro-serializer-7.5.0.jar;"
        "file:///opt/flink-1.20.1/lib/common-config-7.5.0.jar;"
        "file:///opt/flink-1.20.1/lib/common-utils-7.5.0.jar;"
        "file:///opt/flink-1.20.1/lib/avro-1.11.3.jar;"
        "file:///opt/flink-1.20.1/lib/jackson-databind-2.12.7.jar;"
        "file:///opt/flink-1.20.1/lib/jackson-core-2.12.7.jar;"
        "file:///opt/flink-1.20.1/lib/jackson-annotations-2.12.7.jar;"
        "file:///opt/flink-1.20.1/lib/guava-31.1-jre.jar")

    create_bigquery_table()

    # Define Kafka source table with Avro-Confluent format
    t_env.execute_sql(f"""
        CREATE TABLE kafka_source (
            id INT,
            trans_date_trans_time STRING,
            cc_num STRING,
            merchant STRING,
            category STRING,
            amt DOUBLE,
            first STRING,
            last STRING,
            gender STRING,
            street STRING,
            city STRING,
            state STRING,
            zip INT,
            lat DOUBLE,
            `long` DOUBLE,
            city_pop INT,
            job STRING,
            dob STRING,
            trans_num STRING,
            unix_time BIGINT,
            merch_lat DOUBLE,
            merch_long DOUBLE,
            is_fraud INT,
            produced_timestamp BIGINT
        ) WITH (
            'connector' = 'kafka',
            'topic' = '{KAFKA_TOPIC}',
            'properties.bootstrap.servers' = '{KAFKA_BOOTSTRAP_SERVERS}',
            'properties.group.id' = 'flink-group',
            'scan.startup.mode' = 'earliest-offset',
            'format' = 'avro-confluent',
            'avro-confluent.schema-registry.url' = '{SCHEMA_REGISTRY_URL}'
        )
        """)

    table = t_env.from_path("kafka_source")

    # Convert to DataStream and process
    ds = t_env.to_data_stream(table)
    import pandas as pd

    ds.map(lambda row: write_to_bigquery(json.dumps({
        "trans_id": row.trans_num,
        "is_fraud": bool(model.predict(
            pd.DataFrame([[getattr(row, feat) for feat in FEATURES]], columns=FEATURES)
        )[0]),
        "produced_timestamp": row.produced_timestamp,
        "processed_timestamp" : int(time.time()*1000),
        "latency_ms": int(time.time() * 1000)-row.produced_timestamp
    })))
    # Execute the job
    env.execute("Kafka to BigQuery with Model Prediction")

if __name__ == "__main__":
    main()

