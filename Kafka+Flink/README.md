# 📦 Apache Kafka, apache flink, bigquery (GCP) for bigdata project

This is project for bigdata project with kafka, flink simulation. This project stimulate process send data (producer) to kafka and store in bigquery.

![Status](https://img.shields.io/badge/status-active-success)

---

## 📚 Table of Contents

- [🛠️ Installation](#️-installation)
- [🧪 Testing](#-testing)


---

## Installation

### ✅ Prerequisites

- A **Google Cloud Platform (GCP)** account.
- **Six running virtual machines** (VMs).
- **Operating System**: Ubuntu or Debian (recommended).
- **BigQuery Admin JSON Key File**:
  1. Go to **GCP Console** → `IAM & Admin` → `Service Accounts`.
  2. Create a new service account and assign the following roles:
     - `BigQuery Data Editor`
     - `BigQuery Data Owner`
     - `BigQuery Job User`
  3. Generate and download the key file (e.g., `bq-key.json`).
  4. Upload the file to the following paths:
     - `/opt/kafka/secrets/` on the **broker1** VM
     - `/opt/flink/secrets/` on the **Flink** VM
- **Firewall Configuration**:
  - Open the following **TCP ports**: `8081`, `2181`, `9092`.
- Ensure the following tools are installed on each VM:
  - [`git`](https://git-scm.com/)
  - [`pip`](https://pip.pypa.io/en/stable/)

  If not installed, run:
  ```bash
  sudo apt update
  sudo apt install git python3-pip -y


### 🛠️ Setup

#### 1. Clone the repository in each machine
``` bash
cd ~ && git clone https://github.com/nvt18624/Bigdata.git
cd Bigdata
chmod +x install.sh env.sh requirement.sh connector.sh flink.sh
```
#### 2. Create virtual environment in each machine and upload bq-key.json to broker1 and flink: In the env.sh, subtitute variables: ip public, project id, dataset ...

``` bash
source env.sh
scp -i <path_to_private_key> <path_to_bq-key.json> <username>@<ip_broker1>:/opt/kafka/secrets/
scp -i <path_to_private_key> <path_to_bq-key.json> <username>@<ip_flink>:/opt/flink/secrets 
```
#### 3. In zookeeper machine 
``` bash
./install.sh
```
#### 4. In broker machine
``` bash
./install.sh <broker_id = {1,2,3}>
```
#### 5. In zookeeper machine 
``` bash
sudo nohup /opt/confluent-7.9.0/bin/schema-registry-start /opt/confluent-7.9.0/etc/schema-registry/schema-registry.properties > /tmp/schema-registry.log 2>&1 &
```
#### 6. In broker 1 machine: Move bq-key.json file to folder /opt/kafka/secrets
``` bash
sudo nohup /opt/kafka/bin/connect-distributed.sh /opt/kafka/config/connect-distributed.properties > /tmp/connector.log 2>&1 &
curl -X POST -H "Content-Type: application/json" -d @/opt/kafka/connector-config/connect-config.json http://localhost:8083/connectors
```
#### 7. In producer machine
``` bash
./requirement.sh
python3 -m venv env && source env/bin/activate
pip install -r producer_requirement.txt
python producer.py
```

#### 8. In flink machine: move bq-key.json file to folder /opt/flink/secrets
``` bash
./requirement.txt && ./flink.sh 
cd /opt/flink && /bin/taskmanager.sh start
python3 -m venv env
source env/bin/active
python flink.py
```

## 🧪 Testing
### In each machine:

#### Check port open with kafka: 9092, zookeeper: 2181, schema-registry: 8081, flink: 8081
``` bash
sudo netstat -tulnp 
```
#### Check connector in broker 1 
``` bash
curl http://localhost:8083/connectors/bigquery-sink-connector-1/status
```
#### Delete connector in broker 1
```bash
curl -X DELETE http://localhost:8083/connectors/bigquery-sink-connector-1
```
#### Kafka server list topic
```bash
bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```
#### Schema registry in zookeeper
```bash
curl http://<zookeeper_ip>:8081/subjects

```

