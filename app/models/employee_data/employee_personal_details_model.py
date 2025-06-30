from sqlalchemy import (
    Column, String, Date, DateTime, Text, ForeignKey, func, Enum as SqlAlchemyEnum
)
from app.db.base import Base
import enum
import uuid

# =========================
# ENUM DEFINITIONS
# =========================

class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"

class MaritalStatus(str, enum.Enum):
    SINGLE = "single"
    MARRIED = "married"
    DIVORCED = "divorced"
    WIDOWED = "widowed"
    OTHER = "other"

class BloodGroup(str, enum.Enum):
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    AB_POS = "AB+"
    AB_NEG = "AB-"
    O_POS = "O+"
    O_NEG = "O-"
    UNKNOWN = "unknown"

# =========================
# PERSONAL DETAILS MODEL
# =========================

class PersonalDetails(Base):
    __tablename__ = "personal_details"

    employee_personal_details_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    employee_id = Column(String(36), ForeignKey("Auth_employees.employee_id", ondelete="CASCADE"), unique=True, nullable=False)

    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=False)

    gender = Column(SqlAlchemyEnum(Gender), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    marital_status = Column(SqlAlchemyEnum(MaritalStatus), nullable=True)
    nationality = Column(String(50), nullable=True)
    blood_group = Column(SqlAlchemyEnum(BloodGroup), nullable=True)

    personal_contact_number = Column(String(20), nullable=True)
    personal_email = Column(String(100), nullable=True)

    permanent_address = Column(Text, nullable=True)
    current_address = Column(Text, nullable=True)

    emergency_contact_person = Column(String(100), nullable=True)
    emergency_contact_number = Column(String(20), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
