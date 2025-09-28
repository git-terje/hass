#!/usr/bin/env bash
set -e

CONFIG_PATH=/data/options.json
DB_URL=$(jq --raw-output ".db_url" $CONFIG_PATH)

export DATABASE_URL=$DB_URL

echo "[INFO] Using database URL: $DATABASE_URL"

# Init database schema
python3 <<'PYCODE'
from app.database import Base, engine
import sys

try:
    Base.metadata.create_all(bind=engine)
    print("[INFO] Database tables ensured.")
except Exception as e:
    print(f"[ERROR] Database init failed: {e}")
    sys.exit(1)
PYCODE

# Start API
cd /app/backend
uvicorn app.main:app --host 0.0.0.0 --port 8180
