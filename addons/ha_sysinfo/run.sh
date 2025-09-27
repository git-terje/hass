#!/usr/bin/with-contenv bashio
set -e

bashio::log.info "Starting Home Assistant System Info add-on..."

# Kjør Python eller annet script som samler info
python3 /usr/src/app/run.py

bashio::log.info "System info collected successfully."
