from datetime import datetime
from sqlalchemy import Integer, Column, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base
from app.enums.delivery import DeliveryStatus


class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True, index=True)

    donation_id = Column(
        Integer,
        ForeignKey("donations.id"),
        nullable=False,
        unique=True,  # One delivery per donation
    )

    # Volunteer handling the delivery
    volunteer_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,  # Assigned when volunteer accepts
    )

    status = Column(
        Enum(DeliveryStatus),
        default=DeliveryStatus.IN_TRANSIT,
        nullable=False,
    )

    pickup_time = Column(
        DateTime,
        nullable=True,
    )

    delivery_time = Column(
        DateTime,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    donation = relationship(
        "Donation",
        back_populates="delivery"
    )

    volunteer = relationship(
        "User",
        back_populates="deliveries"
    )
