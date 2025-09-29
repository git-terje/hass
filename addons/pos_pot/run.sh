#!/bin/bash
set -e

# Hent database URL fra add-on options.json
DB_URL=$(jq -r .db_url /data/options.json)
if [ -n "$DB_URL" ] && [ "$DB_URL" != "null" ]; then
    export DATABASE_URL="$DB_URL"
else
    export DATABASE_URL="mysql+pymysql://homeassistant:deploy@core-mariadb/homeassistant"
fi

# Sett PYTHONPATH slik at app/ kan importeres riktig
export PYTHONPATH=/app/backend

cd /app/backend

# Start FastAPI via uvicorn, med riktig app-dir (app/ er et package)
exec python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8180 --app-dir /app/backend
