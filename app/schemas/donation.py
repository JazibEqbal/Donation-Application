from datetime import datetime
from pydantic import BaseModel, Field

from app.enums.donation import DonationStatus


class DonationCreate(BaseModel):
    food_name: str = Field(..., min_length=2, max_length=100)
    quantity: int = Field(..., gt=0)
    category: str = Field(..., min_length=2)
    pickup_address: str
    latitude: float
    longitude: float
    expiry_time: datetime


class DonationResponse(BaseModel):
    id: int
    donor_id: int
    food_name: str
    quantity: int
    category: str
    pickup_address: str
    latitude: float
    longitude: float
    expiry_time: datetime
    status: DonationStatus

    class Config:
        from_attributes = True