#!/usr/bin/env sh
echo "Adding cron ..."
crond
echo "Cron daemon started"
python3 /data/web/manage.py crontab remove
echo "Cron removed entries"
python3 /data/web/manage.py crontab remove
echo "Cron added entries"
echo "Adding cron done!"
