#!/usr/bin/with-contenv bashio
set -e

bashio::log.info "Starting HA POS..."

# Start uvicorn direkte som PID 1 (ingen underprosesser som kan feile)
exec uvicorn run:app --host 0.0.0.0 --port 8091
