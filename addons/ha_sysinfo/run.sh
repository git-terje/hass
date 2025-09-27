#!/usr/bin/env bash
set -e

echo "[INFO] Starting Home Assistant System Info add-on..."

OUTDIR="/data"
mkdir -p "$OUTDIR"

# Hent systeminfo via Supervisor API
curl -sSL -H "Authorization: Bearer $SUPERVISOR_TOKEN" \
    http://supervisor/info > "$OUTDIR/sysinfo.json"

# Hent installerte addons
curl -sSL -H "Authorization: Bearer $SUPERVISOR_TOKEN" \
    http://supervisor/addons > "$OUTDIR/addons.json"

# Hent Home Assistant core info
curl -sSL -H "Authorization: Bearer $SUPERVISOR_TOKEN" \
    http://supervisor/core/info > "$OUTDIR/core_info.json"

# Hent integrasjoner (config entries)
curl -sSL -H "Authorization: Bearer $SUPERVISOR_TOKEN" \
    http://supervisor/core/api/config/config_entries/entry \
    -H "Content-Type: application/json" > "$OUTDIR/integrations.json"

# Hent siste 200 linjer fra loggene
curl -sSL -H "Authorization: Bearer $SUPERVISOR_TOKEN" \
    http://supervisor/core/logs | tail -n 200 > "$OUTDIR/logs.txt"

echo "[INFO] System info collected successfully."
