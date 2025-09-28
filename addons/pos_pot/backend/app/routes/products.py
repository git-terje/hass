from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database

router = APIRouter(prefix="/api/products", tags=["products"])

@router.post("/")
def create_product(name: str, category: str, price: float, package_type: str = None, weight_grams: float = None, db: Session = Depends(database.get_db)):
    db_product = models.Product(
        name=name,
        category=category,
        price=price,
        package_type=package_type,
        weight_grams=weight_grams
    )
    db.add(db_product)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Product with this name already exists")
    db.refresh(db_product)
    return db_product

@router.get("/")
def list_products(db: Session = Depends(database.get_db)):
    return db.query(models.Product).all()

@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(database.get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
