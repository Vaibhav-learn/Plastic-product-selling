from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class AreaCreate(BaseModel):
    name : str = Field(min_length = 2, max_length=100)

class AreaResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)