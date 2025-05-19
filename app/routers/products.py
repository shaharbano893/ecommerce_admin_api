# routes/products.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.database.database import get_session
from app.models.models import Products
from app.schemas.schemas import ProductCreate, ProductRead

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ProductRead)
def create_product(product: ProductCreate, session: Session = Depends(get_session)):
    db_product = Products(**product.model_dump())
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@router.get("/", response_model=List[ProductRead])
def read_products(session: Session = Depends(get_session)):
    products = session.exec(select(Products)).all()
    return products

@router.get("/{product_id}", response_model=ProductRead)
def read_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Products, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductRead)
def update_product(product_id: int, product: ProductCreate, session: Session = Depends(get_session)):
    db_product = session.get(Products, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product.model_dump().items():
        setattr(db_product, key, value)
    
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@router.delete("/{product_id}")
def delete_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Products, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    session.delete(product)
    session.commit()
    return {"message": "Product deleted successfully"}
