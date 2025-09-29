ARG BUILD_FROM
FROM $BUILD_FROM

# Installer avhengigheter
RUN apk add --no-cache nodejs npm git

# Klon OpenTHC POS
WORKDIR /app
RUN git clone https://github.com/openthc/pos.git .
RUN npm install

# Eksponer port
EXPOSE 8180

# Start POS
CMD ["npm", "start"]
