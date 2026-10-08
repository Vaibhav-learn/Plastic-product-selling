from pydantic import BaseModel, ConfigDict

from app.models.user import Department, UserRole

class UserResponse(BaseModel):
    id:int
    name:str
    phone:str
    email:str | None
    login_id: str
    role: UserRole
    department: Department | None
    area_id: int | None
    is_active: bool
    must_change_password: bool
    model_config = ConfigDict(from_attributes = True)