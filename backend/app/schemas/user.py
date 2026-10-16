from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.user import Department, UserRole

class UserCreate(BaseModel):
    name : str = Field(min_length=2, max_length=100)
    phone : str = Field(min_length=10, max_length=20)
    email : str | None = None
    login_id : str = Field(min_length=3, max_length = 50)
    password : str = Field(min_length=8, max_length = 72)
    role : UserRole
    department : Department | None = None
    area_id : int | None = None
    @model_validator(mode="after")
    def validate_worker_configuration(self):
        if self.role == UserRole.ADMIN:
            if self.department is not None:
                raise ValueError("Admin cannot have department")

            if self.area_id is not None:
                raise ValueError("Admin cannot have an assigned area")

        return self
            

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
    created_by : int | None
    model_config = ConfigDict(from_attributes = True)
