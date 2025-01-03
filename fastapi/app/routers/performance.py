from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database
from fastapi import BackgroundTasks

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/recalculate")
def recalculate_metrics(background_tasks: BackgroundTasks, db: Session = Depends(database.get_db)):
    background_tasks.add_task(crud.update_all_metrics, db)
    return {"message": "Recalculation started"}

@router.get("/well_performing", response_model=list[schemas.Lead])
def get_well_performing_accounts(db: Session = Depends(database.get_db)):
    """Endpoint to retrieve well-performing accounts."""
    return crud.get_well_performing_accounts(db)

@router.get("/underperforming", response_model=list[schemas.Lead])
def get_underperforming_accounts(db: Session = Depends(database.get_db)):
    """Endpoint to retrieve underperforming accounts."""
    return crud.get_underperforming_accounts(db)

@router.get("/{lead_id}", response_model=schemas.PerformanceMetrics)
def get_performance_metrics(lead_id: int, db: Session = Depends(database.get_db)):
    metrics = crud.get_performance_metrics(db=db, lead_id=lead_id)
    if not metrics:
        raise HTTPException(status_code=404, detail="Performance metrics not found")
    return metrics

@router.put("/{lead_id}", response_model=schemas.PerformanceMetrics)
def update_performance_metrics(lead_id: int, metrics: schemas.PerformanceMetricsBase, db: Session = Depends(database.get_db)):
    return crud.update_performance_metrics(db=db, lead_id=lead_id, metrics=metrics)