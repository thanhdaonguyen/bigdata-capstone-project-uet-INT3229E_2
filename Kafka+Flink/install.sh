#! /bin/bash
./requirement.sh
source env.sh

[ -d /opt/kafka ] || {

path=$(pwd)
wget https://dlcdn.apache.org/kafka/3.9.0/kafka_2.13-3.9.0.tgz 
tar -xvzf kafka_2.13-3.9.0.tgz > /dev/null && sudo mv kafka_2.13-3.9.0 /opt/kafka > /dev/null
echo "Successfull install kafka"
rm -rf "$path/kafka_2.13-3.9.0.tgz"

}

cd /opt/kafka 
[ -n "$1" ] && {

sed -i "s|^zookeeper\.connect=.*|zookeeper.connect=${zookeeper_ip}:2181|" /opt/kafka/config/server.properties
sed -i "s|^broker.id=.*|broker.id=$1|" /opt/kafka/config/server.properties
sed -i "s|^log.dirs=/tmp/kafka-logs.*|log.dirs=/tmp/kafka-logs-$1|" /opt/kafka/config/server.properties

eval "broker_ip=\$broker${1}_ip"
sed -i "s|^#listeners=PLAINTEXT:.*|listeners=PLAINTEXT://0.0.0.0:9092|" /opt/kafka/config/server.properties
sed -i "s|^.*advertised.listeners=PLAINTEXT:.*|advertised.listeners=PLAINTEXT://${broker_ip}:9092|" /opt/kafka/config/server.properties
nohup sudo /opt/kafka/bin/kafka-server-start.sh /opt/kafka/config/server.properties > /tmp/kafka-server.log 2>&1 &

}  || {
## schema -regsitry
nohup sudo /opt/kafka/bin/zookeeper-server-start.sh /opt/kafka/config/zookeeper.properties > /tmp/zookeeper.log 2>&1 &

## install confluet kafka for schema registry
[ ! -d /opt/confluent-7.9.0/ ] && {
cd ~
wget https://packages.confluent.io/archive/7.9/confluent-7.9.0.tar.gz && sudo tar -xvzf confluent-7.9.0.tar.gz > /dev/null
sudo mv confluent-7.9.0 /opt && rm -rf ~/confluent-7*
echo "Install Successfully schema-registry"

}

cd /opt/confluent-7.9.0/
sudo sed -i "s|^kafkastore.bootstrap.servers=PLAINTEXT://.*|kafkastore.bootstrap.servers=PLAINTEXT://${broker1_ip}:9092|" /opt/confluent-7.9.0/etc/schema-registry/schema-registry.properties
# sudo nohup /opt/confluent-7.9.0/bin/schema-registry-start /opt/confluent-7.9.0/etc/schema-registry/schema-registry.properties > /tmp/schema-registry.log 2>&1 &
}

# Install connector if borker is 1 
[ "$1" -eq 1 ] 2>/dev/null && $(bash ~/Bigdata/connector.sh) && echo "Move plugins complete"
