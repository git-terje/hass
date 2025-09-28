from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database

router = APIRouter(prefix="/api/products", tags=["products"])

@router.post("/")
def create_product(name: str, category: str, price: float, db: Session = Depends(database.get_db)):
    db_product = models.Product(name=name, category=category, price=price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/")
def list_products(db: Session = Depends(database.get_db)):
    return db.query(models.Product).all()
