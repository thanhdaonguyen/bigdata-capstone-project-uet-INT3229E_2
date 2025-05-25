#! /bin/bash
sudo apt-get update && sudo apt-get install python3-venv
which java > /dev/null 2>&1

[ ! $? -ne 0 ] || {
sudo apt update && sudo apt install openjdk-17-jdk
cat >> ~/.bashrc << 'EOF'
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
EOF
}

source ~/.bashrc
