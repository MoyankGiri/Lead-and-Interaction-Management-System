from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database
from typing import List

router = APIRouter()

@router.post("/", response_model=schemas.POC)
def create_poc(poc: schemas.POCBase, db: Session = Depends(database.get_db)):
    return crud.create_poc(db=db, poc=poc)

@router.get("/{poc_id}", response_model=schemas.POC)
def get_poc(poc_id: int, db: Session = Depends(database.get_db)):
    return crud.get_poc(db=db, poc_id=poc_id)

@router.get("/", response_model=List[schemas.POC])
def get_all_pocs(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return crud.get_all_pocs(db=db, skip=skip, limit=limit)

@router.delete("/{poc_id}")
def delete_poc(poc_id: int, db: Session = Depends(database.get_db)):
    crud.delete_poc(db=db, poc_id=poc_id)
    return {"message": "POC deleted successfully"}