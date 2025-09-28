from fastapi import FastAPI
from .routes import health, products, resellers
from .database import Base, engine

app = FastAPI()

# Opprett tabeller
Base.metadata.create_all(bind=engine)

# Ruter
app.include_router(health.router)
app.include_router(products.router)
app.include_router(resellers.router)

@app.get("/api")
def root():
    return {"message": "Backend is running"}
