from sqlalchemy import (
    Column, String, Date, DateTime, Text, ForeignKey, func
)
from app.db.base import Base
import uuid

# =========================
# WORK EXPERIENCE MODEL
# =========================

class WorkExperience(Base):
    __tablename__ = "work_experience"
    
    experience_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    employee_id = Column(String(36), ForeignKey("Auth_employees.employee_id", ondelete="CASCADE"), nullable=False)
    
    company_name = Column(String(255), nullable=False)
    job_title = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)  # null if current job
    
    responsibilities = Column(Text, nullable=True)
    achievements = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    
    reference_name = Column(String(255), nullable=True)
    reference_contact = Column(String(20), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<WorkExperience(experience_id={self.experience_id}, employee_id={self.employee_id}, company_name={self.company_name}, job_title={self.job_title})>"