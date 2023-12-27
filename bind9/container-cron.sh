#!/bin/sh
echo "Starting zone update job with ZONE_UPDATE_INTERVAL_SECONDS = $ZONE_UPDATE_INTERVAL_SECONDS"
sleep 30

while true; do
    echo "Running zone update job"
    python3 /conf.py
    rndc reload
    sleep $ZONE_UPDATE_INTERVAL_SECONDS
done
