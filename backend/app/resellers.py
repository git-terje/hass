from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database

router = APIRouter(prefix="/api/resellers", tags=["resellers"])

@router.post("/")
def create_reseller(name: str, db: Session = Depends(database.get_db)):
    db_reseller = models.Reseller(name=name)
    db.add(db_reseller)
    db.commit()
    db.refresh(db_reseller)
    return db_reseller

@router.get("/")
def list_resellers(db: Session = Depends(database.get_db)):
    return db.query(models.Reseller).all()
