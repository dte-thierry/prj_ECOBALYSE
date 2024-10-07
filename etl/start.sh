#!/bin/bash
sleep 5
mkdir -p /app/logs/etl
python3 /app/app.py &> /app/logs/etl/etl_logs_$(date -I)_.txt


