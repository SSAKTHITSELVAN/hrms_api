from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Any
from datetime import datetime
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
# BASE SCHEMA
# =========================

class CompanyBase(BaseModel):
    company_code: str = Field(..., max_length=20, description="Unique company code")
    company_name: str = Field(..., max_length=200, description="Company name")
    company_legal_name: str = Field(..., max_length=300)
    company_logo_url: Optional[str] = Field(None, max_length=500)
    company_website_url: Optional[str] = Field(None, max_length=300)
    company_organization_type: Optional[CompanyOrganizationType]
    company_industry_sector: str = Field(..., max_length=100)
    company_size_category: Optional[CompanySizeCategory]
    company_contact_number: Optional[str] = Field(None, max_length=20)
    company_email: Optional[EmailStr] = Field(None, description="Unique email")
    company_primary_address: Optional[str]
    company_billing_address: Optional[str]
    company_tax_id: Optional[str] = Field(None, max_length=50)
    company_registration_number: Optional[str] = Field(None, max_length=100)
    company_timezone: Optional[str] = Field(None, max_length=50)
    company_locale: Optional[str] = Field(None, max_length=10)
    company_currency: Optional[str] = Field(None, max_length=10)
    company_fiscal_year_start: Optional[int] = Field(None, ge=1, le=12, description="Month (1-12)")
    subscription_tier: Optional[SubscriptionTier]
    subscription_status: Optional[SubscriptionStatus]
    subscription_expires_at: Optional[datetime]
    company_status: CompanyStatus = Field(default=CompanyStatus.ACTIVE)
    onboarding_completed: bool = Field(default=False)
    # compliance_flags: Optional[Any]  # JSON type


# =========================
# CREATE SCHEMA
# =========================

class CompanyCreate(CompanyBase):
    """
    Schema for creating a new company
    """
    pass


# =========================
# UPDATE SCHEMA
# =========================

class CompanyUpdate(BaseModel):
    """
    Schema for updating an existing company
    """
    company_code: Optional[str] = Field(None, max_length=20)
    company_name: Optional[str] = Field(None, max_length=200)
    company_legal_name: Optional[str] = Field(None, max_length=300)
    company_logo_url: Optional[str] = Field(None, max_length=500)
    company_website_url: Optional[str] = Field(None, max_length=300)
    company_organization_type: Optional[CompanyOrganizationType]
    company_industry_sector: Optional[str] = Field(None, max_length=100)
    company_size_category: Optional[CompanySizeCategory]
    company_contact_number: Optional[str] = Field(None, max_length=20)
    company_email: Optional[EmailStr]
    company_primary_address: Optional[str]
    company_billing_address: Optional[str]
    company_tax_id: Optional[str] = Field(None, max_length=50)
    company_registration_number: Optional[str] = Field(None, max_length=100)
    company_timezone: Optional[str] = Field(None, max_length=50)
    company_locale: Optional[str] = Field(None, max_length=10)
    company_currency: Optional[str] = Field(None, max_length=3)
    company_fiscal_year_start: Optional[int] = Field(None, ge=1, le=12)
    subscription_tier: Optional[SubscriptionTier]
    subscription_status: Optional[SubscriptionStatus]
    subscription_expires_at: Optional[datetime]
    company_status: Optional[CompanyStatus]
    onboarding_completed: Optional[bool]
    # compliance_flags: Optional[Any]


# =========================
# RESPONSE SCHEMA
# =========================

class CompanyResponse(CompanyBase):
    company_id: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]
    # created_by: Optional[str]
    # updated_by: Optional[str]
    
    model_config = {"from_attributes": True}  # for pydantic v2

