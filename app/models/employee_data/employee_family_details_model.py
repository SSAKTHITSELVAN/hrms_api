from sqlalchemy import (
    Column, String, Date, DateTime, ForeignKey, Boolean, func
)
from app.db.base import Base
import uuid

class FamilyDetails(Base):
    __tablename__ = "family_details"

    family_details_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = Column(String(36), ForeignKey("Auth_employees.employee_id", ondelete="CASCADE"), unique=True, nullable=False)

    # Father
    is_father = Column(Boolean, default=False, nullable=True)
    father_name = Column(String(100), nullable=True)
    father_date_of_birth = Column(Date, nullable=True)
    father_contact_number = Column(String(20), nullable=True)

    # Mother
    is_mother = Column(Boolean, default=False, nullable=True)
    mother_name = Column(String(100), nullable=True)
    mother_date_of_birth = Column(Date, nullable=True)
    mother_contact_number = Column(String(20), nullable=True)

    # Spouse
    is_spouse = Column(Boolean, default=False, nullable=True)
    spouse_name = Column(String(100), nullable=True)
    spouse_date_of_birth = Column(Date, nullable=True)
    spouse_contact_number = Column(String(20), nullable=True)

    # Child
    is_children = Column(Boolean, default=False, nullable=True)
    children_name = Column(String(100), nullable=True)

    # Sibling
    is_siblings = Column(Boolean, default=False, nullable=True)
    sibling_names = Column(String(100), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True)