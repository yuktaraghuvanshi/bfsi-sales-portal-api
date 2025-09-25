from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class ProductBase(BaseModel):
    key_name: str
    display_name: str
    description: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    key_name: Optional[str]
    display_name: Optional[str]
    description: Optional[str]

from datetime import datetime

class ProductOut(ProductBase):
    product_id: UUID
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

    class Config:
        orm_mode = True
