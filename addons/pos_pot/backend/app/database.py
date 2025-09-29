import os
import pymysql  # Registrerer PyMySQL som driver
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Hent database-URL fra miljøvariabel eller bruk fallback
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://homeassistant:deploy@core-mariadb/homeassistant"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
