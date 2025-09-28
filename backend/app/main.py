from fastapi import FastAPI
from .routes import health

app = FastAPI()

app.include_router(health.router, prefix="/api")

@app.get("/api")
def root():
    return {"message": "Backend is running"}

