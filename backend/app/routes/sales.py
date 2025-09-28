from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database

router = APIRouter(prefix="/api/sales", tags=["sales"])

@router.post("/")
def create_sale(product_id: int, reseller_id: int, quantity: int = 1, db: Session = Depends(database.get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    reseller = db.query(models.Reseller).filter(models.Reseller.id == reseller_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if not reseller:
        raise HTTPException(status_code=404, detail="Reseller not found")

    total_price = product.price * quantity
    sale = models.Sale(product_id=product_id, reseller_id=reseller_id, quantity=quantity, total_price=total_price)

    db.add(sale)
    db.commit()
    db.refresh(sale)
    return {
        "id": sale.id,
        "product": product.name,
        "reseller": reseller.name,
        "quantity": quantity,
        "total_price": total_price,
        "created_at": sale.created_at
    }

@router.get("/")
def list_sales(db: Session = Depends(database.get_db)):
    return db.query(models.Sale).all()
