#! /bin/bash
# Tạo thư mục secrets nếu chưa có
[ ! -d /opt/kafka/secrets ] && mkdir /opt/kafka/secrets
[ ! -d /opt/kafka/connector-config ] && mkdir /opt/kafka/connector-config

envsubst < ~/Bigdata/connect-config-template.json > /opt/kafka/connector-config/connect-config.json

# Copy plugins
cp -r ~/Bigdata/plugins /opt/kafka/
# echo "Move plugins connector complete"


# Ghi file config Kafka Connect
cd /opt/kafka/
bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic ${topic_send} --replication-factor 3 --partitions 1
bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic connect-offsets --replication-factor 3 --partitions 1
bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic connect-configs --replication-factor 3 --partitions 1
bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic connect-status --replication-factor 3 --partitions 1

cat > config/connect-distributed.properties << 'EOF'
bootstrap.servers=localhost:9092
group.id=connect-cluster

# Chỉ định nơi lưu trữ offset, status, config
offset.storage.topic=connect-offsets
offset.storage.replication.factor=3
config.storage.topic=connect-configs
config.storage.replication.factor=3
status.storage.topic=connect-status
status.storage.replication.factor=3

# REST API port (mặc định 8083)
rest.port=8083

# Converters cho key và value (dùng JSON hoặc Avro)
key.converter=org.apache.kafka.connect.storage.StringConverter
value.converter=org.apache.kafka.connect.json.JsonConverter
value.converter.schemas.enable=false

# Paths chứa plugins/connector
plugin.path=/opt/kafka/plugins
EOF

