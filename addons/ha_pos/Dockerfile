ARG BUILD_FROM=ghcr.io/hassio-addons/base:15.0.6
FROM ${BUILD_FROM}

WORKDIR /usr/src/app

# Installer Python og pip
RUN apk add --no-cache python3 py3-pip

# Kopier requirements og installer (med override for PEP 668)
COPY requirements.txt ./
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Kopier app-kode og oppstartsscript
COPY run.py ./
COPY run.sh /run.sh
RUN chmod a+x /run.sh

# Standard kommando
CMD [ "/run.sh" ]
