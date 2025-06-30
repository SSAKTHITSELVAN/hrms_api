from sqlalchemy import (
    Column, String, DateTime, ForeignKey, Boolean, func, Enum as SqlAlchemyEnum
)
from app.db.base import Base
import enum
import uuid

# =========================
# ENUM DEFINITIONS
# =========================

class AddressType(str, enum.Enum):
    PERMANENT = "permanent"
    CURRENT = "current"
    WORK = "work"

# =========================
# ADDRESS MODEL
# =========================

class Address(Base):
    __tablename__ = "employee_address"

    address_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    employee_id = Column(String(36), ForeignKey("Auth_employees.employee_id", ondelete="CASCADE"),  nullable=False)

    address_type = Column(SqlAlchemyEnum(AddressType), nullable=False)

    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255), nullable=True)

    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), nullable=False)

    is_current = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
