ARG BUILD_FROM=ghcr.io/hassio-addons/base:15.0.6
FROM ${BUILD_FROM}

WORKDIR /usr/src/app

# Kopier run.sh
COPY run.sh /run.sh
RUN chmod a+x /run.sh

# Default kommando
CMD [ "/run.sh" ]
