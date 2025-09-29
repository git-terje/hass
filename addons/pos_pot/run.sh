#!/bin/bash
set -e

# Hent database URL fra add-on options.json
export DATABASE_URL=$(jq -r .db_url /data/options.json)

# Sett PYTHONPATH slik at app/ kan importeres riktig
export PYTHONPATH=/app/backend

cd /app/backend

# Start FastAPI via uvicorn gjennom Python, med riktig app-dir
exec python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8180 --app-dir /app/backend
