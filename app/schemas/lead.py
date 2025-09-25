from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class LeadBase(BaseModel):
    customer_id: UUID
    product_id: UUID
    assigned_to: Optional[UUID] = None
    status: Optional[str] = "new"          # new, in_progress, closed
    priority: Optional[int] = 2            # 1=high,2=normal,3=low
    source: Optional[str] = "web"
    notes: Optional[str] = None

class LeadCreate(LeadBase):
    pass

class LeadUpdate(BaseModel):
    assigned_to: Optional[UUID] = None
    status: Optional[str] = None
    priority: Optional[int] = None
    source: Optional[str] = None
    notes: Optional[str] = None

class LeadOut(LeadBase):
    lead_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
