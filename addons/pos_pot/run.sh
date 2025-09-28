#!/usr/bin/env bash
cd /app/backend
uvicorn app.main:app --host 0.0.0.0 --port 8180
