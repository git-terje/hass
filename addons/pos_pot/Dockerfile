FROM python:3.11-slim

# Installer systemavhengigheter
RUN apt-get update && apt-get install -y gcc libmariadb-dev-compat libmariadb-dev jq \
    && rm -rf /var/lib/apt/lists/*

# Sett arbeidsmappe
WORKDIR /app

# Kopier backend-kode inn i add-on image
COPY ./backend /app/backend
COPY ./backend/requirements.txt /app/backend/

# Installer Python-deps
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Kopier run.sh (riktig sti!)
COPY run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 8180
CMD [ "/run.sh" ]
