# app/models/customer.py
import uuid
from sqlalchemy import Column, String, Date, Text, ForeignKey, TIMESTAMP, func, Index
from sqlalchemy.dialects.postgresql import UUID
from app.db import Base

class Customer(Base):
    __tablename__ = "customers"
    customer_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=True)
    email = Column(String(254), nullable=True)   # unique only if provided
    phone = Column(String(20), nullable=True)
    dob = Column(Date, nullable=True)
    address = Column(Text, nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        # Partial unique index: unique on email but only where email IS NOT NULL
        Index("ux_customers_email", "email", unique=True, postgresql_where=(email != None)),
        Index("idx_customers_phone", "phone"),
    )
