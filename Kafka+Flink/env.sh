#! /bin/bash

export zookeeper_ip=localhost
export broker1_ip=localhost
export broker2_ip=localhost
export broker3_ip=localhost
export topic_send="<topic_name>"
export project_id="<project_id>"
export dataset="<dataset_name>"
export csv_path="<path_to_csv_gg_cloud>"

export CONFLUENT_HOME=/opt/confluent-7.9.0
export PATH=$PATH:$CONFLUENT_HOME/bin
