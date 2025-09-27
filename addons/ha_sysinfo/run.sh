#!/usr/bin/with-contenv bashio
set -e

bashio::log.info "Starting Home Assistant System Info add-on..."

# Samle systeminformasjon
OS=$(uname -a)
CPU=$(cat /proc/cpuinfo | grep 'model name' | head -1 | cut -d':' -f2-)
MEM=$(free -h | grep Mem | awk '{print $2 " total, " $3 " used, " $4 " free"}')
DISK=$(df -h / | tail -1 | awk '{print $2 " total, " $3 " used, " $4 " free"}')

# Logg resultatet
bashio::log.info "OS: $OS"
bashio::log.info "CPU:$CPU"
bashio::log.info "Memory: $MEM"
bashio::log.info "Disk: $DISK"

# (Valgfritt) eksponer JSON til en fil som kan leses av HA eller API
cat <<EOF > /data/sysinfo.json
{
  "os": "$OS",
  "cpu": "$CPU",
  "memory": "$MEM",
  "disk": "$DISK"
}
EOF

bashio::log.info "System info written to /data/sysinfo.json"

# Hold containeren i live så HA kan vise loggene
tail -f /dev/null
