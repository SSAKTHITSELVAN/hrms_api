from fastapi import Depends
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from app.tasks.jwt_utils import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_access_token(token)
        return payload  # you can return full payload or user id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )