#!/bin/sh
python3 /conf.py || exit 1

echo named.conf ------------------------------------------------
cat  /etc/bind/named.conf
echo
echo upstream.conf ---------------------------------------------
cat  /etc/bind/upstream.conf
echo
echo domains.conf ----------------------------------------------
cat  /etc/bind/domains.conf
echo
echo rndc.conf -------------------------------------------------
cat  /etc/bind/rndc.conf
echo
echo -----------------------------------------------------------
echo "Starting zone update job..."
/container-cron.sh &
echo "Starting named..."
named -g -u named
