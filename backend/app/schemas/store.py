from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from app.models.store import StoreStatus

class StoreCreate(BaseModel):
    name: str = Field(min_length = 2, max_length=100)
    owner_name: str = Field(min_length = 2, max_length = 100)
    phone: str = Field(min_length = 10, max_length = 13)
    alternate_phone: str = Field(min_length = 10, max_length = 13)
    address: str = Field(min_length=5)
    city : str = Field(min_length=2, max_length=50)
    state : str = Field(min_length=2, max_length=50)
    pincode : str = Field(min_length=2, max_length=6)
    gst_number: str | None = None
    notes: str | None = None
    area_id: int


class StoreResponse(BaseModel):
    id:int
    name: str
    owner_name : str
    phone : str
    alternate_phone : str
    address : str
    city : str
    state: str
    pincode: str
    gst_number: str | None
    notes : str | None
    area_id : int
    created_by : None
    status : StoreStatus
    reviewed_by: int | None
    review_note : str | None
    reviewd_at : datetime | None

    created_at: datetime
    updated_at : datetime
    model_config =ConfigDict(from_attributes=True)
