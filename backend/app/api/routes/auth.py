from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserResponse

router = APIRouter(prefix ="/auth", tags = ["Authentication"])
@router.post("/login", response_model = TokenResponse)

def login(data : LoginRequest, db: Session = Depends(get_db),):
    statement = select(User).where(User.login_id == data.login_id)

    user = db.scalar(statement)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail ="Invalid login ID or password",)

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Invalid login ID or password",)

    if not user.is_active:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = "User account is inactive",)

    token = create_access_token(user_id=user.id, role=user.role.value)

    return TokenResponse(access_token = token)

@router.get("/me", response_model = UserResponse)

def get_me(current_user : User = Depends(get_current_user)):
    return current_user
