from sqlalchemy import (
    Column, String, DateTime, func, Enum as SqlAlchemyEnum, Boolean,
    Integer, JSON, ForeignKey
)
from app.db.base import Base
import uuid
import enum


# =========================
# ENUM DEFINITIONS
# =========================

class CompanyOrganizationType(str, enum.Enum):
    CORPORATION = "CORPORATION"
    LLC = "LLC"
    PARTNERSHIP = "PARTNERSHIP"
    NON_PROFIT = "NON_PROFIT"
    GOVERNMENT = "GOVERNMENT"
    STARTUP = "STARTUP"

class CompanySizeCategory(str, enum.Enum):
    ONE_TO_TEN = "1-10"
    ELEVEN_TO_FIFTY = "11-50"
    FIFTY_ONE_TO_TWO_HUNDRED = "51-200"
    TWO_HUNDRED_ONE_TO_THOUSAND = "201-1000"
    ABOVE_THOUSAND = "1000+"

class SubscriptionTier(str, enum.Enum):
    BASIC = "BASIC"
    PROFESSIONAL = "PROFESSIONAL"
    ENTERPRISE = "ENTERPRISE"

class SubscriptionStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    TRIAL = "TRIAL"
    EXPIRED = "EXPIRED"

class CompanyStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"
    ARCHIVED = "ARCHIVED"


# =========================
# COMPANY MODEL
# =========================

class Company(Base):
    __tablename__ = "Company"

    company_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_code = Column(String(20), nullable=False, unique=True)
    company_name = Column(String(200), nullable=False)
    company_legal_name = Column(String(300), nullable=False)
    company_logo_url = Column(String(500), nullable=True)
    company_website_url = Column(String(300), nullable=True)
    company_organization_type = Column(SqlAlchemyEnum(CompanyOrganizationType), nullable=False)
    company_industry_sector = Column(String(100), nullable=False)
    company_size_category = Column(SqlAlchemyEnum(CompanySizeCategory), nullable=False)
    company_contact_number = Column(String(20), nullable=True)
    company_email = Column(String(320), nullable=False)
    company_primary_address = Column(String, nullable=True)
    company_billing_address = Column(String, nullable=True)
    company_tax_id = Column(String(50), nullable=True)
    company_registration_number = Column(String(100), nullable=True)
    company_timezone = Column(String(50), nullable=True)
    company_locale = Column(String(10), nullable=True)
    company_currency = Column(String(10), nullable=True)
    company_fiscal_year_start = Column(Integer, nullable=True)
    subscription_tier = Column(SqlAlchemyEnum(SubscriptionTier), nullable=True)
    subscription_status = Column(SqlAlchemyEnum(SubscriptionStatus), nullable=True)
    subscription_expires_at = Column(DateTime(timezone=True), nullable=True)
    company_status = Column(SqlAlchemyEnum(CompanyStatus), nullable=False, default=CompanyStatus.ACTIVE)
    onboarding_completed = Column(Boolean, nullable=False, default=False)
    # compliance_flags = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # created_by = Column(String(36), ForeignKey("employee_details.employee_id"), nullable=True)
    # updated_by = Column(String(36), ForeignKey("employee_details.employee_id"), nullable=True)
