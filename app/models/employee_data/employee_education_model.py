from sqlalchemy import (
    Column, String, Date, DateTime, ForeignKey, Boolean, func, Text
)
from app.db.base import Base
import uuid

class Education(Base):
    __tablename__ = "education"

    education_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = Column(String(36), ForeignKey("Auth_employees.employee_id", ondelete="CASCADE"), nullable=False)

    institution_name = Column(String(255), nullable=False)
    institution_location = Column(String(255), nullable=True)

    degree_name = Column(String(100), nullable=False)
    field_of_study = Column(String(100), nullable=True)
    education_level = Column(String(50), nullable=False)  # E.g., Bachelor, Master
    mode_of_study = Column(String(50), nullable=True)  # Full-time, Part-time

    start_date = Column(Date, nullable=True)
    completion_date = Column(Date, nullable=True)

    percentage_or_grade = Column(String(50), nullable=True)

    is_highest_qualification = Column(Boolean, default=False)

    additional_notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
