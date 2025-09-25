from sqlalchemy.orm import Session
from uuid import UUID
from sqlalchemy.exc import IntegrityError
from app.models import Product
from app.schemas.product import ProductCreate, ProductUpdate

def get_product(db: Session, product_id: UUID):
    return db.query(Product).filter(Product.product_id == product_id).first()

def list_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()

def create_product(db: Session, product_in: ProductCreate):
    db_product = Product(
        key_name=product_in.key_name,
        display_name=product_in.display_name,
        description=product_in.description
    )
    db.add(db_product)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError(f"Product with key_name '{product_in.key_name}' already exists.")
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: UUID, product_in: ProductUpdate):
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    if not db_product:
        return None
    for field, value in product_in.dict(exclude_unset=True).items():
        setattr(db_product, field, value)
    try:
        db.commit()
        db.refresh(db_product)
        return db_product
    except IntegrityError as e:
        db.rollback()
        if 'products_key_name_key' in str(e.orig):
            raise ValueError(f"Product key_name '{product_in.key_name}' already exists." if product_in.key_name else "Duplicate key_name error")
        raise

def delete_product(db: Session, product_id: UUID):
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product
