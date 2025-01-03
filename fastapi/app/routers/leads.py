from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database
from typing import List
import logging

router = APIRouter()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@router.post("/", response_model=schemas.Lead)
def create_lead(lead: schemas.LeadCreate, db: Session = Depends(database.get_db)):
    logging.debug(f"Create lead in leads.py {lead}")
    return crud.create_lead(db=db, lead=lead)

@router.get("/due_today", response_model=List[schemas.Lead])
def get_due_calls_today(db: Session = Depends(database.get_db)):
    """Endpoint to retrieve leads requiring calls today."""
    return crud.get_leads_requiring_calls_today(db)

@router.get("/", response_model=List[schemas.Lead])
def get_all_leads(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_all_leads(db=db, skip=skip, limit=limit)

@router.get("/{lead_id}", response_model=schemas.Lead)
def get_lead(lead_id: int, db: Session = Depends(database.get_db)):
    lead = crud.get_lead(db=db, lead_id=lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@router.put("/{lead_id}", response_model=schemas.LeadBase)
def update_lead(lead_id: int, lead_data: schemas.LeadUpdate, db: Session = Depends(database.get_db)):
    """Endpoint to update a lead."""
    updated_lead = crud.update_lead(db, lead_id, lead_data)
    if not updated_lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return updated_lead

@router.delete("/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(database.get_db)):
    crud.delete_lead(db=db, lead_id=lead_id)
    return {"message": "Lead deleted successfully"}
