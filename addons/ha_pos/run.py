import os
import json
import logging
from fastapi import FastAPI, HTTPException
from google.oauth2 import service_account
from googleapiclient.discovery import build
from cachetools import TTLCache
import pandas as pd
import uvicorn

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ha_pos")

app = FastAPI(title="HA Point of Sales")

# Load add-on config
CONFIG_FILE = "/data/options.json"
if not os.path.exists(CONFIG_FILE):
    raise RuntimeError("Missing /data/options.json, add-on cannot start")

with open(CONFIG_FILE) as f:
    CONFIG = json.load(f)

CREDENTIALS_FILE = CONFIG.get("credentials_file")
SHEET_ID = CONFIG.get("sheet_id")
WORKSHEET = CONFIG.get("worksheet")

# Setup Google API
try:
    CREDS = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"],
    )
    SERVICE = build("sheets", "v4", credentials=CREDS, cache_discovery=False)
    logger.info("Google Sheets API initialized successfully")
except Exception as e:
    SERVICE = None
    logger.error(f"Could not initialize Google API: {e}")

# Cache: 10 entries, TTL 60s
CACHE = TTLCache(maxsize=10, ttl=60)

def fetch_sheet(sheet_id: str, worksheet: str) -> pd.DataFrame:
    """Fetch worksheet into DataFrame, with caching"""
    cache_key = f"{sheet_id}:{worksheet}"
    if cache_key in CACHE:
        return CACHE[cache_key]

    try:
        result = (
            SERVICE.spreadsheets()
            .values()
            .get(spreadsheetId=sheet_id, range=worksheet)
            .execute()
        )
        rows = result.get("values", [])
        if not rows:
            return pd.DataFrame()
        df = pd.DataFrame(rows[1:], columns=rows[0])
        CACHE[cache_key] = df
        return df
    except Exception as e:
        logger.error(f"Failed to fetch sheet {sheet_id}/{worksheet}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/config")
async def get_config():
    return {"sheet_id": SHEET_ID, "worksheet": WORKSHEET}

@app.get("/api/worksheets")
async def list_worksheets(sheet_id: str = None):
    sid = sheet_id or SHEET_ID
    try:
        metadata = SERVICE.spreadsheets().get(spreadsheetId=sid).execute()
        return [ws["properties"]["title"] for ws in metadata["sheets"]]
    except Exception as e:
        logger.error(f"Error listing worksheets for {sid}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/products")
async def get_products(sheet_id: str = None, worksheet: str = None):
    sid = sheet_id or SHEET_ID
    ws = worksheet or WORKSHEET
    df = fetch_sheet(sid, ws)
    return df.to_dict(orient="records")

if __name__ == "__main__":
    port = int(os.environ.get("INGRESS_PORT", 8091))
    uvicorn.run(app, host="0.0.0.0", port=port)
