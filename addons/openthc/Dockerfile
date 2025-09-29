ARG BUILD_FROM=ghcr.io/home-assistant/base:14.1.1
FROM $BUILD_FROM

# Installer avhengigheter
RUN apk add --no-cache \
    nodejs \
    npm \
    git \
    bash

# Sett opp arbeidsdir
WORKDIR /app

# Hent OpenTHC POS kildekode
RUN git clone https://github.com/openthc/pos.git /app

# Installer avhengigheter
RUN npm install

# Bygg frontend hvis nødvendig
RUN npm run build || true

# Expose ingress-port
EXPOSE 8280

# Startscript
COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD [ "/run.sh" ]
