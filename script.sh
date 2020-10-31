#!/bin/bash
(crontab -l ; echo "0 */3 * * * echo '' > /opt/ofa-ips/poc_traffic.txt")| crontab -

echo -e "/var/lib/docker/containers/*/*.log {
 rotate 3
 daily
 compress
 size=50M
 missingok
 delaycompress
 copytruncate
}" > docker-logs
