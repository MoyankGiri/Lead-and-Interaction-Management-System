from pydantic import BaseModel
from typing import Optional
from datetime import date

# ------------------------------
# Lead Schemas
# ------------------------------
class LeadBase(BaseModel):
    restaurant_name: str
    address: Optional[str]
    status: str
    call_frequency: Optional[int]
    last_call_date: Optional[date]

class LeadCreate(BaseModel):
    restaurant_name: str
    address: str
    status: str
    call_frequency: int
    last_call_date: Optional[date]

    class Config:
        orm_mode = True

class Lead(LeadBase):
    lead_id: int

    class Config:
        orm_mode = True

class LeadUpdate(BaseModel):
    restaurant_name: Optional[str]
    address: Optional[str]
    status: Optional[str]
    call_frequency: Optional[int]
    last_call_date: Optional[date]

# ------------------------------
# POC Schemas
# ------------------------------
class POCBase(BaseModel):
    lead_id: int
    name: str
    role: Optional[str]
    phone: Optional[str]
    email: Optional[str]

class POC(POCBase):
    poc_id: int

    class Config:
        orm_mode = True

# ------------------------------
# Interaction Schemas
# ------------------------------
class InteractionBase(BaseModel):
    lead_id: int
    interaction_date: date
    details: Optional[str]
    order_placed: Optional[bool] = False

class Interaction(InteractionBase):
    interaction_id: int

    class Config:
        orm_mode = True

# ------------------------------
# Performance Metrics Schemas
# ------------------------------
class PerformanceMetricsBase(BaseModel):
    order_frequency: Optional[int]
    last_order_date: Optional[date]
    performance_status: Optional[str]

class PerformanceMetrics(PerformanceMetricsBase):
    performance_id: int
    lead_id: int

    class Config:
        orm_mode = True

# ------------------------------
# User Schemas
# ------------------------------
class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    user_id: int
    username: str
    role: str

    class Config:
        orm_mode = True