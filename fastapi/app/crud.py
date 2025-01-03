from sqlalchemy.orm import Session
from app import models, schemas
from datetime import datetime, timezone, timedelta
import logging
from sqlalchemy import func, text, or_

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# -------------------------------
# CRUD Operations for Leads
# -------------------------------
def create_lead(db: Session, lead: schemas.LeadCreate):
    db_lead = models.Lead(**lead.dict())
    logger.debug(f"inside crud create lead: {db_lead}")
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

def get_lead(db: Session, lead_id: int):
    return db.query(models.Lead).filter(models.Lead.lead_id == lead_id).first()

def get_all_leads(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Lead).order_by(models.Lead.lead_id).offset(skip).limit(limit).all()

def update_lead(db: Session, lead_id: int, lead: schemas.LeadCreate):
    db_lead = db.query(models.Lead).filter(models.Lead.lead_id == lead_id).first()
    if not db_lead:
        return None
    for key, value in lead.dict().items():
        setattr(db_lead, key, value)
    db.commit()
    db.refresh(db_lead)
    return db_lead

def delete_lead(db: Session, lead_id: int):
    db_lead = db.query(models.Lead).filter(models.Lead.lead_id == lead_id).first()
    if db_lead:
        db.delete(db_lead)
        db.commit()

def get_leads_requiring_calls_today(db: Session):
    """Retrieve leads requiring calls today."""
    today = func.current_date()
    return db.query(models.Lead).filter(
        (models.Lead.last_call_date == None) |  # Leads never called
        (today >= models.Lead.last_call_date + text("CAST(call_frequency AS INTEGER) * interval '1 day'"))
    ).all()

# -------------------------------
# CRUD Operations for POCs
# -------------------------------
def create_poc(db: Session, poc: schemas.POCBase):
    db_poc = models.POC(**poc.dict())
    db.add(db_poc)
    db.commit()
    db.refresh(db_poc)
    return db_poc

def get_poc(db: Session, poc_id: int):
    return db.query(models.POC).filter(models.POC.poc_id == poc_id).first()

def get_all_pocs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.POC).offset(skip).limit(limit).all()

def delete_poc(db: Session, poc_id: int):
    db_poc = db.query(models.POC).filter(models.POC.poc_id == poc_id).first()
    if db_poc:
        db.delete(db_poc)
        db.commit()

# -------------------------------
# CRUD Operations for Interactions
# -------------------------------
# def create_interaction(db: Session, interaction: schemas.InteractionBase):
#     db_interaction = models.Interaction(**interaction.dict())
#     db.add(db_interaction)
#     db.commit()
#     db.refresh(db_interaction)
#     return db_interaction

def create_interaction(db: Session, interaction: schemas.InteractionBase):
    db_interaction = models.Interaction(**interaction.dict())
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)

    # Update performance metrics for the lead
    performance_metrics = calculate_performance_metrics(db, db_interaction.lead_id)
    if performance_metrics:
        update_performance_metrics(db, db_interaction.lead_id, performance_metrics)

    return db_interaction

def get_interaction(db: Session, lead_id: int):
    return db.query(models.Interaction).filter(models.Interaction.lead_id == lead_id).all()

def get_all_interactions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Interaction).offset(skip).limit(limit).all()

# -------------------------------
# CRUD Operations for Performance Metrics
# -------------------------------
def get_performance_metrics(db: Session, lead_id: int):

    performance_metrics = calculate_performance_metrics(db, lead_id)
    if performance_metrics:
        update_performance_metrics(db, lead_id, performance_metrics)

    return db.query(models.PerformanceMetrics).filter(models.PerformanceMetrics.lead_id == lead_id).first()

def update_performance_metrics(db: Session, lead_id: int, metrics: dict):
    existing_metrics = db.query(models.PerformanceMetrics).filter(models.PerformanceMetrics.lead_id == lead_id).first()

    if existing_metrics:
        # Update existing record
        existing_metrics.order_frequency = metrics["order_frequency"]
        existing_metrics.last_order_date = metrics["last_order_date"]
        existing_metrics.performance_status = metrics["performance_status"]
    else:
        # Create new record
        new_metrics = models.PerformanceMetrics(
            lead_id=lead_id,
            order_frequency=metrics["order_frequency"],
            last_order_date=metrics["last_order_date"],
            performance_status=metrics["performance_status"]
        )
        db.add(new_metrics)

    db.commit()

def update_all_metrics(db: Session):
    leads = db.query(models.Lead).all()
    for lead in leads:
        metrics = calculate_performance_metrics(db, lead.lead_id)
        if metrics:
            update_performance_metrics(db, lead.lead_id, metrics)

def calculate_performance_metrics(db: Session, lead_id: int):
    """Calculate performance metrics for a given lead."""
    interactions = db.query(models.Interaction).filter(models.Interaction.lead_id == lead_id).all()
    
    if not interactions:
        return {
            "order_frequency": 0,
            "last_order_date": None,
            "performance_status": "Underperforming",
        }

    # Calculate total orders and order frequency
    total_orders = sum(1 for interaction in interactions if interaction.order_placed)
    order_frequency = total_orders / max(len(interactions), 1)  # Average orders per interaction

    # Find the last order date
    last_order_date = max(
        (interaction.interaction_date for interaction in interactions if interaction.order_placed),
        default=None
    )

    # Current date
    today = datetime.now(timezone.utc).date()

    # Determine performance status based on new criteria
    if last_order_date and (today - last_order_date).days <= 15 and total_orders > 5:
        performance_status = "Well-performing"
    elif last_order_date is None or (today - last_order_date).days > 30 or total_orders <= 1:
        performance_status = "Underperforming"
    else:
        performance_status = "Average"

    return {
        "order_frequency": total_orders,  # Total orders (frequency calculation optional)
        "last_order_date": last_order_date,
        "performance_status": performance_status,
    }

def get_well_performing_accounts(db: Session):
    """Retrieve well-performing accounts based on predefined criteria."""
    thirty_days_ago = datetime.now(timezone.utc).date() - timedelta(days=30)
    fifteen_days_ago = datetime.now(timezone.utc).date() - timedelta(days=15)

    return db.query(models.Lead).join(models.PerformanceMetrics).filter(
        models.PerformanceMetrics.order_frequency > 5,  # High order frequency
        models.PerformanceMetrics.last_order_date >= fifteen_days_ago,  # Recent orders
    ).all()

def get_underperforming_accounts(db: Session):
    """Retrieve underperforming accounts based on predefined criteria."""
    thirty_days_ago = datetime.now(timezone.utc).date() - timedelta(days=30)

    return db.query(models.Lead).join(models.PerformanceMetrics).filter(
        or_(
            models.PerformanceMetrics.order_frequency <= 1,  # Low order frequency
            models.PerformanceMetrics.last_order_date < thirty_days_ago,  # Older orders
        )
    ).all()

# -------------------------------
# Authentication-related Operations
# -------------------------------
def create_user(db: Session, username: str, hashed_password: str):
    db_user = models.User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def verify_password(plain_password: str, hashed_password: str):
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)