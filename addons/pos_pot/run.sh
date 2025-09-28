#!/usr/bin/env bash
CONFIG_PATH=/data/options.json
DB_URL=$(jq --raw-output ".db_url" $CONFIG_PATH)

export DATABASE_URL=$DB_URL

cd /app/backend
uvicorn app.main:app --host 0.0.0.0 --port 8180
