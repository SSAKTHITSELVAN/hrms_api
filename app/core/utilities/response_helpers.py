# response_helpers.py
from fastapi import status
from typing import Any
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pydantic.json import pydantic_encoder
import json

def success_response(data=None, message="Success", code=611):
    # If data is Pydantic model or list of models, convert to dicts
    if isinstance(data, BaseModel):
        data = data.dict()
    elif isinstance(data, list):
        data = [item.dict() if isinstance(item, BaseModel) else item for item in data]
    
    response = {
        "success": True,
        "message": message,
        "status_code": code,
        "data": data
    }
    # Use pydantic_encoder to handle datetime, UUID, etc.
    return json.loads(json.dumps(response, default=pydantic_encoder))


def error_response(message: str, error_code: str = None, details: Any = None):
    return JSONResponse(
        content={
            "success": False,
            "message": message,
            "error_code": error_code,
            "details": details
        }
    )
