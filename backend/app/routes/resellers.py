from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database

router = APIRouter(prefix="/api/resellers", tags=["resellers"])

@router.post("/")
def create_reseller(name: str, db: Session = Depends(database.get_db)):
    db_reseller = models.Reseller(name=name)
    db.add(db_reseller)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Reseller with this name already exists")
    db.refresh(db_reseller)
    return db_reseller

@router.get("/")
def list_resellers(db: Session = Depends(database.get_db)):
    return db.query(models.Reseller).all()

@router.get("/{reseller_id}")
def get_reseller(reseller_id: int, db: Session = Depends(database.get_db)):
    reseller = db.query(models.Reseller).filter(models.Reseller.id == reseller_id).first()
    if not reseller:
        raise HTTPException(status_code=404, detail="Reseller not found")
    return reseller
