from fastapi import FastAPI
from app.core.database import engine
from app.db.base import Base
from app.models.organization.company_model import Company
from app.models.organization.department_model import Department
from app.models.organization.role_model import Role
from app.models.authentication.auth_employee import Employee
from app.models.employee_data.employee_personal_details_model import PersonalDetails
from app.models.employee_data.employee_address_model import Address
from app.models.employee_data.employee_education_model import Education
from app.models.employee_data.employee_family_details_model import FamilyDetails
from app.models.employee_data.employee_emergency_contacts_model import EmergencyContact

from app.organization import company_router
from app.department import department_router
from app.role import role_router
from app.authentication import authentication_router, login_router
from app.employee_management.employee_personal_details import personal_details_router
from app.employee_management.employee_address import address_router
from app.employee_management.employee_education import education_router
from app.employee_management.employee_family_details import family_details_router
from app.employee_management.employee_emergency_contacts import emergency_contacts_router

from fastapi import FastAPI, Request
from app.core.utilities.exceptions.base import AppException
from app.core.constants import ErrorCode
from app.core.utilities.response_helpers import error_response

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# List of origins that should be allowed to make cross-origin requests
origins = [
    "http://localhost:3000",  # your React app (dev)
    "http://127.0.0.1:3000",
    "http://localhost:5173",  # production frontend
]

# Apply the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["*"] for all
    allow_credentials=False,
    allow_methods=["*"],  # allow all HTTP methods like GET, POST
    allow_headers=["*"],  # allow all headers
)



app.include_router(company_router.router, prefix="/api/v1")
app.include_router(department_router.router)
app.include_router(role_router.router, prefix="/api/v1")
app.include_router(authentication_router.router)
app.include_router(login_router.router, prefix="/api/v1")
app.include_router(personal_details_router.router, prefix="/api/v1")
app.include_router(address_router.router, prefix="/api/v1")
app.include_router(education_router.router, prefix="/api/v1")
app.include_router(family_details_router.router, prefix="/api/v1")
app.include_router(emergency_contacts_router.router, prefix="/api/v1")

@app.get("/")
async def hrms():
    code = "HRMS API IS WORKING WELL!"
    return code



@app.on_event('startup')
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.exception_handler(AppException)
async def handle_app_exception(request: Request, exc: AppException):
    message = exc.message_key
    return error_response(
        message=exc.message_key,
        error_code=exc.status_code,
        details=exc.details
    )

@app.exception_handler(Exception)
async def handle_unexpected_exception(request: Request, exc: Exception):
    return error_response(
        message= "UNHANDLED_EXCEPTION",
        error_code= 500,
        details=str(exc)
    )