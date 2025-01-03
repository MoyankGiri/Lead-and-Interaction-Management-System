from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="admin")  # Roles like 'admin' or 'user' can be added

class Lead(Base):
    __tablename__ = "leads"
    lead_id = Column(Integer, primary_key=True, index=True)
    restaurant_name = Column(String, nullable=False)
    address = Column(String)
    status = Column(String, nullable=False)
    call_frequency = Column(Integer)
    last_call_date = Column(Date)
    pocs = relationship("POC", back_populates="lead")
    interactions = relationship("Interaction", back_populates="lead")
    performance = relationship("PerformanceMetrics", back_populates="lead", uselist=False)

class POC(Base):
    __tablename__ = "pocs"
    poc_id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.lead_id"), nullable=False)
    name = Column(String, nullable=False)
    role = Column(String)
    phone = Column(String)
    email = Column(String)
    lead = relationship("Lead", back_populates="pocs")

class Interaction(Base):
    __tablename__ = "interactions"
    interaction_id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.lead_id"), nullable=False)
    interaction_date = Column(Date, nullable=False)
    details = Column(String)
    order_placed = Column(Boolean, default=False)
    lead = relationship("Lead", back_populates="interactions")

class PerformanceMetrics(Base):
    __tablename__ = "performancemetrics"
    performance_id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.lead_id"), nullable=False)
    order_frequency = Column(Integer)
    last_order_date = Column(Date)
    performance_status = Column(String)
    lead = relationship("Lead", back_populates="performance")