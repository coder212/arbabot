#!/bin/bash
uptimes=$(uptime)
temper=$(cat /etc/armbianmonitor/datasources/soctemp)
echo -e " uptime: $uptimes \n "$temper°C
