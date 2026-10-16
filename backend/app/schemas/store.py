from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from app.models.store import StoreStatus

class StoreCreate(BaseModel):
    name: str = Field(min_length = 2, max_length=100)
    owner_name: str = Field(min_length = 2, max_length = 100)
    phone: str = Field()