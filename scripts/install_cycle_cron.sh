#!/usr/bin/env bash
set -e
source /opt/atlas/venv/bin/activate
cd /opt/atlas || exit 1

CRON_LINE="0 */6 * * * /opt/atlas/scripts/run_day_of_brahma.sh >> /opt/atlas/logs/day_of_brahma.log 2>&1"

mkdir -p /opt/atlas/logs

( crontab -l 2>/dev/null | grep -v 'run_day_of_brahma.sh' ; echo "$CRON_LINE" ) | crontab -

echo "Installed cycle cron:"
echo "$CRON_LINE"
