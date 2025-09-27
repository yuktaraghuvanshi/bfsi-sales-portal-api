from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from app.models.product import Product  # assuming this exists

from app import crud
from app.db import get_db
from app.schemas import customer as customer_schemas


router = APIRouter(prefix="/customers", tags=["customers"])


import logging

logging.basicConfig(level=logging.DEBUG)



@router.post("/", response_model=customer_schemas.CustomerOut)
def create_customer(
    customer: customer_schemas.CustomerCreate, 
    db: Session = Depends(get_db), 
    user_id: Optional[UUID] = None
):
    logging.debug(f"user_id={user_id}, customer={customer}")
    try:
        return crud.customer.create_customer(db, customer, user_id)
    except IntegrityError as e:
        db.rollback()  # rollback the failed transaction
        if 'ux_customers_email' in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email '{customer.email}' already exists."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
@router.get("/", response_model=list[customer_schemas.CustomerOut])
def get_customers(
    skip: int = 0, 
    limit: int = 100, 
    user_id: Optional[UUID] = None,  # Make optional
    db: Session = Depends(get_db)
):
    return crud.customer.list_customers(db, skip, limit, user_id)

# Customers per product using Leads table
@router.get("/count-by-product")
def customers_per_product(db: Session = Depends(get_db)):
    # Check if Leads table has entries
    results = (
        db.query(Product.name, func.count(func.distinct(Lead.customer_id)))
        .join(Lead, Lead.product_id == Product.product_id)
        .group_by(Product.name)
        .all()
    )
    return [{"product": r[0], "total_customers": r[1]} for r in results]


@router.get("/{customer_id}", response_model=customer_schemas.CustomerOut)
def get_customer(customer_id: UUID, db: Session = Depends(get_db)):
    db_customer = crud.customer.get_customer(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer


@router.put("/{customer_id}", response_model=customer_schemas.CustomerOut)
def update_customer(customer_id: UUID, customer: customer_schemas.CustomerUpdate, db: Session = Depends(get_db)):
    updated = crud.customer.update_customer(db, customer_id, customer)
    if not updated:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated


@router.delete("/{customer_id}", response_model=customer_schemas.CustomerOut)
def delete_customer(customer_id: UUID, db: Session = Depends(get_db)):
    deleted = crud.customer.delete_customer(db, customer_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Customer not found")
    return deleted

