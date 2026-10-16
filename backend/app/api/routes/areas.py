from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_admin
from app.core.database import get_db
from app.models.area import Area
from app.models.user import User
from app.schemas.area import AreaCreate, AreaResponse

router = APIRouter(prefix="/areas", tags=["Areas"],)

@router.post("", response_model=AreaResponse, status_code=status.HTTP_201_CREATED,)
def create_area(data : AreaCreate, db: Session = Depends(get_db), current_admin: User = Depends(require_admin)):
    existing_area = db.scalar(select(Area).where(Area.name == data.name))

    if existing_area is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Area already exists",)

    area = Area(name = data.name)
    db.add(Area)
    try:
        db.commit()

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail ="Area exists")

    db.refresh(area)
    return area

@router.get("", response_model=list[AreaResponse],)
def get_areas(db: Session = Depends(get_db),current_user: User = Depends(get_current_user),):
    areas = db.scalars(select(Area).order_by(Area.name)).all()
    return areas