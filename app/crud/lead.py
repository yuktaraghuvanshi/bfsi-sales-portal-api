from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from app import models
from app.schemas.lead import LeadCreate, LeadUpdate

def get_lead(db: Session, lead_id: UUID):
    return db.query(models.Lead).filter(models.Lead.lead_id == lead_id).first()

def list_leads(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Lead).offset(skip).limit(limit).all()

def create_lead(db: Session, lead_in: LeadCreate):
    # Validate foreign keys
    customer = db.query(models.Customer).filter(models.Customer.customer_id == lead_in.customer_id).first()
    if not customer:
        raise ValueError(f"customer_id '{lead_in.customer_id}' does not exist.")
    
    product = db.query(models.Product).filter(models.Product.product_id == lead_in.product_id).first()
    if not product:
        raise ValueError(f"product_id '{lead_in.product_id}' does not exist.")
    
    if lead_in.assigned_to:
        user = db.query(models.User).filter(models.User.user_id == lead_in.assigned_to).first()
        if not user:
            raise ValueError(f"assigned_to user_id '{lead_in.assigned_to}' does not exist.")

    lead = models.Lead(
        customer_id=lead_in.customer_id,
        product_id=lead_in.product_id,
        assigned_to=lead_in.assigned_to,
        status=lead_in.status,
        priority=lead_in.priority,
        source=lead_in.source,
        notes=lead_in.notes
    )
    db.add(lead)
    try:
        db.commit()
        db.refresh(lead)
        return lead
    except IntegrityError as e:
        db.rollback()
        raise ValueError(f"Error creating lead: {str(e.orig)}")

def update_lead(db: Session, lead_id: UUID, lead_in: LeadUpdate):
    lead = db.query(models.Lead).filter(models.Lead.lead_id == lead_id).first()
    if not lead:
        return None

    data = lead_in.dict(exclude_unset=True)

    # Validate foreign keys if provided
    if "customer_id" in data:
        customer = db.query(models.Customer).filter(models.Customer.customer_id == data["customer_id"]).first()
        if not customer:
            raise ValueError(f"customer_id '{data['customer_id']}' does not exist.")
    
    if "product_id" in data:
        product = db.query(models.Product).filter(models.Product.product_id == data["product_id"]).first()
        if not product:
            raise ValueError(f"product_id '{data['product_id']}' does not exist.")

    if "assigned_to" in data and data["assigned_to"]:
        user = db.query(models.User).filter(models.User.user_id == data["assigned_to"]).first()
        if not user:
            raise ValueError(f"assigned_to user_id '{data['assigned_to']}' does not exist.")

    for field, value in data.items():
        setattr(lead, field, value)

    try:
        db.commit()
        db.refresh(lead)
        return lead
    except IntegrityError as e:
        db.rollback()
        raise ValueError(f"Error updating lead: {str(e.orig)}")

def delete_lead(db: Session, lead_id: UUID):
    lead = db.query(models.Lead).filter(models.Lead.lead_id == lead_id).first()
    if lead:
        db.delete(lead)
        db.commit()
    return lead
