from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    password = Column(String, nullable=False)

    role = Column(String, nullable=False)

    # One user can create many donations
    donations = relationship(
        "Donation",
        back_populates="donor"
    )

    requests = relationship(
        "DonationRequest",
        back_populates="requester"
    )

    deliveries = relationship(
        "Delivery",
        back_populates="volunteer"
    )