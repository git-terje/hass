ARG BUILD_FROM=ghcr.io/home-assistant/base:14.1.1
FROM ${BUILD_FROM}

# Installer avhengigheter
RUN apk add --no-cache \
    python3 \
    py3-pip \
    jq \
    mariadb-connector-c-dev \
    build-base

# Kopier backend
COPY backend /app/backend
COPY run.sh /app/run.sh

# Gjør run.sh kjørbar
RUN chmod a+x /app/run.sh

# Legg til service-fil for s6-overlay
COPY rootfs/ /

# Bruk s6-overlay som init
CMD [ "/init" ]
