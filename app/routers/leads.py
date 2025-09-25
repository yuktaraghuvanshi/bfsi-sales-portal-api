from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app import crud
from app.db import get_db
from app.schemas import lead as lead_schemas

router = APIRouter(prefix="/leads", tags=["leads"])

@router.post("/", response_model=lead_schemas.LeadOut)
def create_lead(lead: lead_schemas.LeadCreate, db: Session = Depends(get_db)):
    try:
        return crud.lead.create_lead(db, lead)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[lead_schemas.LeadOut])
def get_leads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.lead.list_leads(db, skip, limit)

@router.get("/{lead_id}", response_model=lead_schemas.LeadOut)
def get_lead(lead_id: UUID, db: Session = Depends(get_db)):
    lead = crud.lead.get_lead(db, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@router.put("/{lead_id}", response_model=lead_schemas.LeadOut)
def update_lead(lead_id: UUID, lead: lead_schemas.LeadUpdate, db: Session = Depends(get_db)):
    updated = crud.lead.update_lead(db, lead_id, lead)
    if not updated:
        raise HTTPException(status_code=404, detail="Lead not found")
    return updated

@router.delete("/{lead_id}", response_model=lead_schemas.LeadOut)
def delete_lead(lead_id: UUID, db: Session = Depends(get_db)):
    deleted = crud.lead.delete_lead(db, lead_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Lead not found")
    return deleted
