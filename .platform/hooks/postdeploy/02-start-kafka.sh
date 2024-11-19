#!/bin/bash

# Kafka Consumer 서비스 파일 생성 및 권한 설정
cat << EOF > /etc/systemd/system/kafka_consumer.service
[Unit]
Description=Kafka Consumer Service
After=network.target

[Service]
User=nobody
Group=nobody
WorkingDirectory=/var/app/current
ExecStart=/bin/bash -c 'source /var/app/venv/*/bin/activate && python3 manage.py consume'
EnvironmentFile=/opt/elasticbeanstalk/support/envvars
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# 서비스 파일 권한 설정
chmod 644 /etc/systemd/system/kafka_consumer.service
chown root:root /etc/systemd/system/kafka_consumer.service

# jq 설치
yum install -y jq

# 환경 변수 파일 생성
mkdir -p /opt/elasticbeanstalk/support && /opt/elasticbeanstalk/bin/get-config environment | jq -r 'to_entries | .[] | "\(.key)=\(.value)"' > /opt/elasticbeanstalk/support/envvars
chmod 644 /opt/elasticbeanstalk/support/envvars
chown root:root /opt/elasticbeanstalk/support/envvars

# systemd 데몬 다시 로드
systemctl daemon-reload

# Kafka Consumer 서비스 활성화 및 시작
systemctl enable kafka_consumer.service
systemctl restart kafka_consumer.service
