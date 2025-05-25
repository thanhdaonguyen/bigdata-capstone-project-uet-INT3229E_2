#! /bin/bash
cd ~

wget https://downloads.apache.org/flink/flink-1.20.1/flink-1.20.1-bin-scala_2.12.tgz
tar -xvzf flink-1.20.1-bin-scala_2.12.tgz
mv flink-1.20.1-bin-scala_2.12.tgz /opt/flink
mv ~/Bigdata/flink.py /opt/flink
mv ~/Bigdata/flink_requirement.txt /opt/flink

rm -rf ~/flink-1.20.1-bin-scala_2.12*

cd /opt/flink
mkdir secrets
