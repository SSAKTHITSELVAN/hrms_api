import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, func, Enum as SqlAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from datetime import datetime
import enum
from app.db.base import Base


# =========================
# ENUM DEFINITIONS
# =========================

class EmployeeStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class Employee(Base):
    __tablename__ = "Auth_employees"
    
    employee_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    company_id = Column(String(36), ForeignKey("Company.company_id"), nullable=False)

    employee_code = Column(String, nullable=False)  # Auto-generated login ID

    employee_department_id = Column(String(36), ForeignKey("Department.department_id"), nullable=False)

    employee_role_id = Column(String(36), ForeignKey("Role.role_id"), nullable=False)

    employee_hashed_password = Column(String, nullable=False)  # Store hashed password

    employee_status = Column(SqlAlchemyEnum(EmployeeStatus), nullable=False)  # status: active, inactive, etc...

    employee_added_by = Column(String(36), ForeignKey("Auth_employees.employee_id"), nullable=True)

    employee_added_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    employee_modified_time = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
