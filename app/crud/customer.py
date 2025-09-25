from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from app import models
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerOut


def get_customer(db: Session, customer_id: UUID):
    return db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()


def list_customers(db: Session, skip: int = 0, limit: int = 100, user_id: Optional[UUID] = None):
    query = db.query(models.Customer)
    if user_id:
        query = query.filter(models.Customer.created_by == user_id)  # Assuming created_by stores the user ID
    return query.offset(skip).limit(limit).all()


def create_customer(db: Session, customer_in: CustomerCreate, user_id: Optional[UUID] = None):
    if customer_in.email:
        existing = db.query(models.Customer).filter(models.Customer.email == customer_in.email).first()
        if existing:
            raise ValueError(f"Email {customer_in.email} already exists")

    db_customer = models.Customer(
        first_name=customer_in.first_name,
        last_name=customer_in.last_name,
        email=customer_in.email,
        phone=customer_in.phone,
        dob=customer_in.dob,
        address=customer_in.address,
        created_by=user_id
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, customer_id: UUID, customer_in: CustomerUpdate):
    db_customer = db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()
    if not db_customer:
        return None
    for field, value in customer_in.dict(exclude_unset=True).items():
        setattr(db_customer, field, value)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def delete_customer(db: Session, customer_id: UUID):
    db_customer = db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()
    if db_customer:
        db.delete(db_customer)
        db.commit()
    return db_customer
