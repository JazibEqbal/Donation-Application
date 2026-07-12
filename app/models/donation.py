from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, Float, String, DateTime, Enum
from sqlalchemy.orm import relationship

from app.database import Base
from app.enums.donation import DonationStatus


class Donation(Base):
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True)

    donor_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    food_name = Column(String, nullable=False)

    quantity = Column(Integer, nullable=False)

    category = Column(String, nullable=False)

    pickup_address = Column(String, nullable=False)

    latitude = Column(Float, nullable=False)

    longitude = Column(Float, nullable=False)

    expiry_time = Column(DateTime, nullable=False)

    status = Column(
        Enum(DonationStatus),
        nullable=False,
        default=DonationStatus.AVAILABLE,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    # Donation belongs to one user
    donor = relationship(
        "User",
        back_populates="donations"
    )

    requests = relationship(
        "DonationRequest",
        back_populates="donation"
    )

    delivery = relationship(
        "Delivery",
        back_populates="donation"
    )
