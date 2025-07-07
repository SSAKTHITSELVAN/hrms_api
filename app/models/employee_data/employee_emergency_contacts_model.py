from sqlalchemy import (
    Column, String, Integer, DateTime, Text, ForeignKey, func, Index
)
from app.db.base import Base
import uuid


# =========================
# EMERGENCY CONTACTS MODEL
# =========================

class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"
    
    contact_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    employee_id = Column(
        String(36), 
        ForeignKey("Auth_employees.employee_id", ondelete="CASCADE"), 
        nullable=False
    )
    
    name = Column(String(100), nullable=True)
    relationship = Column(String(50), nullable=True)
    
    primary_phone = Column(String(20), nullable=True)
    secondary_phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    
    priority_order = Column(Integer, default=1, nullable=True)
    
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=True
    )
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=True
    )
    
    # Indexes
    __table_args__ = (
        Index('idx_emergency_contacts_employee_id', 'employee_id'),
        Index('idx_emergency_contacts_priority_order', 'priority_order'),
    )