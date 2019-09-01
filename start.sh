#!/usr/bin/env bash

# . deploy/config.sh

docker stop $(docker ps -q --filter ancestor=py-api.cwg.tw )

docker build -t py-api.cwg.tw -f Dockerfile .

docker run -v /app/logs:/app/logs/ -p 5000:5000 -e TZ=Asia/Taipei -d py-api.cwg.tw

