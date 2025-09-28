FROM python:3.11-slim

# Backend avhengigheter
WORKDIR /app
COPY backend/ /app/backend
COPY backend/requirements.txt /app/backend/
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Frontend bygg (hvis du bruker npm/yarn)
WORKDIR /app/frontend
COPY frontend/ /app/frontend
RUN apt-get update && apt-get install -y nodejs npm
RUN npm install && npm run build

# Kjør backend + serve frontend
WORKDIR /app
COPY addons/ha_pos/run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 8180
CMD [ "/run.sh" ]
