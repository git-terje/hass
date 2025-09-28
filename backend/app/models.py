from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    category = Column(String, nullable=False)  # flower, edible, etc
    package_type = Column(String, nullable=True)  # unopened, opened
    price = Column(Float, nullable=False)
    weight_grams = Column(Float, nullable=True)

    sales = relationship("Sale", back_populates="product")


class Reseller(Base):
    __tablename__ = "resellers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    active = Column(Boolean, default=True)

    sales = relationship("Sale", back_populates="reseller")


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    reseller_id = Column(Integer, ForeignKey("resellers.id"))
    quantity = Column(Integer, nullable=False, default=1)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    product = relationship("Product", back_populates="sales")
    reseller = relationship("Reseller", back_populates="sales")
