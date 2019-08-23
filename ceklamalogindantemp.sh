#!/bin/bash
uptimes=$(uptime)
temp=$(cat /sys/class/thermal/thermal_zone0/temp)
temper=$(($temp/1000))
echo -e " uptime: $uptimes \n "$temper °C
