#!/usr/bin/env bash
CONFIG_PATH=/data/options.json
DB_URL=$(jq --raw-output ".db_url" $CONFIG_PATH)

export DATABASE_URL=$DB_URL
export PYTHONPATH=/app/backend  # viktig for at uvicorn finner app.main

cd /app/backend
uvicorn app.main:app --host 0.0.0.0 --port 8180
