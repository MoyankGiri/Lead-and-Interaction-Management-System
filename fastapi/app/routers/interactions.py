from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database
from typing import List

router = APIRouter()

@router.post("/", response_model=schemas.Interaction)
def create_interaction(interaction: schemas.InteractionBase, db: Session = Depends(database.get_db)):
    return crud.create_interaction(db=db, interaction=interaction)

@router.get("/{lead_id}", response_model=List[schemas.Interaction])
def get_interaction(lead_id: int, db: Session = Depends(database.get_db)):
    return crud.get_interaction(db=db, lead_id=lead_id)

@router.get("/", response_model=List[schemas.Interaction])
def get_all_interactions(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return crud.get_all_interactions(db=db, skip=skip, limit=limit)