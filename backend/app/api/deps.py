from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User, UserRole, Department

bearer_scheme = HTTPBearer()

def get_current_user(credentials : HTTPAuthorizationCredentials = Depends(bearer_scheme), db : Session = Depends(get_db),)-> User:
    token = credentials.credentials

    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid or expired access token",)

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid access token",)

    try:
        user_id = int(user_id)

    except(TypeError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Invalid access token",)


    user = db.get(User, user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not exist",)

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=  "User account is inactive",)

    return user

def require_admin(current_user : User = Depends(get_current_user),)-> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = "Admin access required",)

    return current_user;

def require_operations(current_user : User = Depends(get_current_user),) -> User:
    if current_user.role == UserRole.ADMIN:
        return current_user

    if current_user.role != UserRole.OFFICE_WORKER or current_user.department != Department.OPERATIONS:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = "Operations access required",)
    return current_user

def require_finance(current_user : User = Depends(get_current_user),) -> User:
    if(current_user.role == UserRole.OFFICE_WORKER or current_user.department != Department.FINANCE) :
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = " Finance access required",)

    return current_user

def require_hr(current_user : User = Depends(get_current_user),) ->User:
    if current_user.role == UserRole.ADMIN:
        return current_user

    if(current_user.role != UserRole.OFFICE_WORKER or current_user.department!= Department.HR):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = "HR access required",)
    return current_user

def require_outside_corker(current_user : User =Depends(get_current_user),) -> User:
    if current_user.role == UserRole.ADMIN:
        return current_user

    if current_user.role != UserRole.Worker:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Outside worker access required",)
    return current_user