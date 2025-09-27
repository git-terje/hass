ARG BUILD_FROM=ghcr.io/hassio-addons/base:15.0.6
FROM ${BUILD_FROM}

WORKDIR /usr/src/app

# Installer Python og dependencies
RUN apk add --no-cache python3 py3-pip

# Kopier requirements og installer (med override)
COPY requirements.txt ./
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Kopier app-kode
COPY run.py ./

# Default kommando
CMD ["python3", "run.py"]
