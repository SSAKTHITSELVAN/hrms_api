from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    employee_code: str = Field(..., description="Unique login code assigned to employee")
    password: str = Field(..., description="User entered password")


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
