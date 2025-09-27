ARG BUILD_FROM=ghcr.io/hassio-addons/base:15.0.6
FROM ${BUILD_FROM}

WORKDIR /usr/src/app

# Installer Python hvis nødvendig
RUN apk add --no-cache python3 py3-pip

# Kopier kode og run.sh
COPY run.py ./
COPY run.sh /run.sh
RUN chmod a+x /run.sh

# Default kommando
CMD [ "/run.sh" ]
