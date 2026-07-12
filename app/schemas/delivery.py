from datetime import datetime
from pydantic import BaseModel

from app.enums.delivery import DeliveryStatus


class DeliveryResponse(BaseModel):
    id: int
    donation_id: int
    volunteer_id: int | None
    status: DeliveryStatus
    pickup_time: datetime | None
    delivery_time: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True
