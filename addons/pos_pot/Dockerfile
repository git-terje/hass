FROM python:3.11-slim

# Installer systemavhengigheter
RUN apt-get update && apt-get install -y gcc libmariadb-dev-compat libmariadb-dev jq \
    && rm -rf /var/lib/apt/lists/*

# Sett arbeidsmappe
WORKDIR /app

# Kopier backend
COPY backend/ /app/backend
COPY backend/requirements.txt /app/backend/

# Installer Python dependencies
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Kopier run.sh
COPY run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 8180
CMD [ "/run.sh" ]

ENV PYTHONPATH=/app/backend
