# app/models/lead.py
import uuid
from sqlalchemy import Column, String, SmallInteger, Text, TIMESTAMP, func, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from app.db import Base

class Lead(Base):
    __tablename__ = "leads"
    lead_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.customer_id", ondelete="CASCADE"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.product_id"), nullable=False)
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True)
    status = Column(String(20), nullable=False, server_default="new")      # allowed: new, in_progress, closed
    priority = Column(SmallInteger, nullable=False, server_default="2")    # 1=high,2=normal,3=low
    source = Column(String(80), server_default="web")
    notes = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        Index("idx_leads_status", "status"),
        Index("idx_leads_product", "product_id"),
    )
