from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.core.database import get_db
from app.core.security import hash_password
from app.models.area import Area
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix ="/workers", tags = ["Workers"])

@router.post("", response_model = UserResponse, status_code=status.HTTP_201_CREATED,)
def create_worker(data : UserCreate, db : Session = Depends(get_db),current_admin : User = Depends(require_admin),):
    existing_user = db.scalar(select(User).where(or_(User.login_id == data.login_id, User.phone == data.phone,)))

    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = "Login ID or phone number already exists",)

    if data.area_id is not None:
        area = db.get(Area, data.area_id)

        if area is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Assigned area does not exist",)

    password_hash = hash_password(data.password)

    user = User(name = data.name, phone = data.phone, email = data.email, login_id = data.login_id, password_hash = password_hash, must_change_password = True, role = data.role, department = data.department,
                area_id = data.area_id, is_active = True, created_by = current_admin.id,)

    db.add(user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = "Login ID or phone number alrady exists",)

    db.refresh(user)
    return user