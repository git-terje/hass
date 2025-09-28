# Home Assistant add-on Dockerfile for POS Pot

# Bruk Home Assistant sitt baseimage
ARG BUILD_FROM
FROM $BUILD_FROM

# Installer systemavhengigheter (Alpine-pakker)
RUN apk add --no-cache \
    python3 \
    py3-pip \
    jq \
    mariadb-connector-c-dev \
    build-base

# Sett arbeidsmappe
WORKDIR /app

# Kopier backend og installer Python dependencies
COPY backend/ /app/backend
RUN pip3 install --no-cache-dir -r /app/backend/requirements.txt

# Kopier run.sh
COPY run.sh /run.sh
RUN chmod +x /run.sh

# Sørg for at uvicorn finner FastAPI-app
ENV PYTHONPATH=/app/backend

EXPOSE 8180
CMD [ "/run.sh" ]
