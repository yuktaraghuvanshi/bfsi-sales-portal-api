from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app import crud
from app.db import get_db
from app.schemas import product as product_schemas

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=product_schemas.ProductOut)
def create_product(product: product_schemas.ProductCreate, db: Session = Depends(get_db)):
    try:
        return crud.product.create_product(db, product)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=List[product_schemas.ProductOut])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.product.list_products(db, skip, limit)

@router.get("/{product_id}", response_model=product_schemas.ProductOut)
def get_product(product_id: UUID, db: Session = Depends(get_db)):
    db_product = crud.product.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=product_schemas.ProductOut)
def update_product(product_id: UUID, product: product_schemas.ProductUpdate, db: Session = Depends(get_db)):
    try:
        updated = crud.product.update_product(db, product_id, product)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@router.delete("/{product_id}", response_model=product_schemas.ProductOut)
def delete_product(product_id: UUID, db: Session = Depends(get_db)):
    deleted = crud.product.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return deleted
