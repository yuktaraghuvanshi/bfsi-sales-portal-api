from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import date
from datetime import datetime
class CustomerBase(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    dob: Optional[date] = None
    address: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass  # All validation handled by Base

class CustomerUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    dob: Optional[date]
    address: Optional[str]

class CustomerOut(CustomerBase):
    customer_id: UUID
    created_by: Optional[UUID]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
