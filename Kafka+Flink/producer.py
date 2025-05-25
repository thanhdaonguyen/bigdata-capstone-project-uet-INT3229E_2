from concurrent.futures import ThreadPoolExecutor, as_completed
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer
import pandas as pd
from datetime import datetime
import time
import os

def update_latency_to_bigquery(latency):

    # Cập nhật độ trễ vào BigQuery
    # Giả sử bạn đã có một hàm để cập nhật độ trễ vào BigQuery
    pass


def delivery_report(err, msg):
    if err is not None:
        print(f"❌ Delivery failed: {err}")
    else:
        print(f"✅ Delivered to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}")

schema_str = """
{
  "type": "record",
  "name": "Transaction",
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "trans_date_trans_time", "type": "string"},
    {"name": "cc_num", "type": "string"},
    {"name": "merchant", "type": "string"},
    {"name": "category", "type": "string"},
    {"name": "amt", "type": "double"},
    {"name": "first", "type": "string"},
    {"name": "last", "type": "string"},
    {"name": "gender", "type": "string"},
    {"name": "street", "type": "string"},
    {"name": "city", "type": "string"},
    {"name": "state", "type": "string"},
    {"name": "zip", "type": "int"},
    {"name": "lat", "type": "double"},
    {"name": "long", "type": "double"},
    {"name": "city_pop", "type": "int"},
    {"name": "job", "type": "string"},
    {"name": "dob", "type": "string"},
    {"name": "trans_num", "type": "string"},
    {"name": "unix_time", "type": "long"},
    {"name": "merch_lat", "type": "double"},
    {"name": "merch_long", "type": "double"},
    {"name": "is_fraud", "type": "int"},
    {"name": "produced_timestamp", "type": "long"}
  ]
}
"""

schema_registry_conf = {'url': 'http://' + os.environ.get('zookeeper_ip', 'localhost') + ':8081'}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)
avro_serializer = AvroSerializer(schema_registry_client, schema_str)

producer_conf = {
        'bootstrap.servers': os.environ.get('broker1_ip', 'localhost')+ ':9092',
    'key.serializer': StringSerializer('utf_8'),
    'value.serializer': avro_serializer,
    'queue.buffering.max.messages': 1000000,
    'queue.buffering.max.kbytes': 2097152,  # 2GB
    'linger.ms': 10,
    'batch.num.messages': 10000
}
producer = SerializingProducer(producer_conf)

# Đọc toàn bộ file CSV
csv_path = os.environ.get("csv_path", "default_path") 
df = pd.read_csv(csv_path)

# Gửi từng dòng với buffer xử lý chặt chẽ
def send_transaction(transaction):
    try:
        # Chuẩn hóa dữ liệu cần thiết
        transaction["trans_date_trans_time"] = datetime.now().isoformat()
        transaction["cc_num"] = str(transaction.get("cc_num", "0000000000000000"))
        transaction["zip"] = int(transaction.get("zip", 0))
        transaction["is_fraud"] = int(transaction.get("is_fraud", 0))
        transaction["produced_timestamp"] = int(time.time() * 1000)

        if transaction is None or any(v is None for v in transaction.values()):
            print(f"⚠️ Bỏ qua transaction ID {transaction.get('id')} vì có giá trị null")
            return

        transaction_id = transaction.get("id")

        for attempt in range(5):
            try:
                producer.produce(
                    topic="transactions_input_1",
                    key=str(transaction_id),
                    value=transaction,
                    on_delivery=delivery_report
                )
                producer.poll(0)
                break
            except BufferError:
                time.sleep(0.2)
    except Exception as e:
        print(f"❌ Lỗi transaction ID {transaction.get('id')}: {e}")

start = datetime.now()

batch_size = 4
rate_limit = 100 # số lượng transaction tối đa mỗi giây
send = 0
total_sent = 0
now = time.time()

for i in range(0, len(df), batch_size):
    df_batch = df[i:i + batch_size]

    # Nếu gửi batch này mà vượt giới hạn 8/s → cắt bớt lại cho vừa
    if send + len(df_batch) > rate_limit:
        df_batch = df_batch.iloc[:rate_limit - send]

    print(f"🚀 Gửi batch {i} ➜ {i + len(df_batch)}...")

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(send_transaction, row.to_dict()) for _, row in df_batch.iterrows()]
        for future in as_completed(futures):
            pass

    producer.flush()
    send += len(df_batch)
    total_sent += len(df_batch)
    print(f"✅ Đã gửi {total_sent}/{len(df)} transactions")

    # Nếu đã đủ giới hạn 8 transaction/s → chờ đến giây tiếp theo
    if send >= rate_limit:
        while time.time() - now < 1.0:
            time.sleep(0.01)  # ngủ một chút để không dùng CPU nhiều
        now = time.time()
        send = 0  # reset lại số lượng đã gửi trong giây mới

end = datetime.now()

print("----------------------------------------------------------------------------------------------------------------")
print(f"🎉 Đã gửi toàn bộ {total_sent} transaction trong {end - start}")
print("----------------------------------------------------------------------------------------------------------------")

