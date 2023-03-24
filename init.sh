#!/bin/sh

CMD="python /app/dodns.py"
STDOUT="/proc/1/fd/1 2>&1"
CRONDIR="/etc/cron.d"
DODNS_CRONFILE="$CRONDIR/dodns-crontab"

if [ -z "${DODNS_SCHEDULE}" ]; then
    export DODNS_SCHEDULE="*/5 * * * *"
fi

echo "Initializing dodns with schedule: $DODNS_SCHEDULE"

echo "Writing dodns cron file to: $DODNS_CRONFILE"

if [ ! -f $DODNS_CRONFILE ]; then
    mkdir -p $CRONDIR
    touch $DODNS_CRONFILE
fi

echo "$DODNS_SCHEDULE $CMD > $STDOUT" > $DODNS_CRONFILE
chmod 0644 $DODNS_CRONFILE
crontab $DODNS_CRONFILE

echo "Starting dodns..."

crond -f
