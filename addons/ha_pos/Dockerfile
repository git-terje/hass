ARG BUILD_FROM=ghcr.io/hassio-addons/base:15.0.6
FROM ${BUILD_FROM}

WORKDIR /usr/src/app

# Installer nødvendige Python-pakker
RUN apk add --no-cache python3 py3-pip
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY run.py ./

CMD ["python3", "run.py"]
