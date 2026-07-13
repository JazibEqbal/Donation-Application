from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.enums.delivery import DeliveryStatus
from app.enums.donation import DonationStatus
from app.models.delivery import Delivery
from app.models.user import User


def _get_delivery(
    db: Session,
    delivery_id: int,
) -> type[Delivery]:

    delivery = db.get(Delivery, delivery_id)

    if delivery is None:
        raise HTTPException(
            status_code=404,
            detail="Delivery not found",
        )

    return delivery


def accept_delivery(
    db: Session,
    delivery_id: int,
    volunteer: User,
) -> type[Delivery]:

    # Find delivery
    delivery = _get_delivery(db, delivery_id)

    # check if the delivery is already assigned or not
    if delivery.volunteer_id is not None:
        raise HTTPException(
            status_code=400,
            detail="Delivery already assigned",
        )

    # Assign volunteer
    delivery.volunteer_id = volunteer.id

    db.commit()
    db.refresh(delivery)

    return delivery


def pickup_delivery(
    db: Session,
    delivery_id: int,
    volunteer: User,
) -> type[Delivery]:

    delivery = _get_delivery(db, delivery_id)

    if delivery.volunteer_id != volunteer.id:
        raise HTTPException(
            status_code=403,
            detail="You are not assigned to this delivery",
        )

    # Pickup allowed only once
    if delivery.status != DeliveryStatus.ASSIGNED:
        raise HTTPException(
            status_code=400,
            detail="Delivery cannot be picked up",
        )

    delivery.pickup_time = datetime.utcnow()

    db.commit()
    db.refresh(delivery)

    return delivery


def mark_delivered(
    db: Session,
    delivery_id: int,
    volunteer: User,
) -> type[Delivery]:

    delivery = _get_delivery(db, delivery_id)

    if delivery.volunteer_id != volunteer.id:
        raise HTTPException(
            status_code=403,
            detail="You are not assigned to this delivery",
        )

    # Delivery must be picked up first
    if delivery.status != DeliveryStatus.PICKED_UP:
        raise HTTPException(
            status_code=400,
            detail="Food has not been picked up yet",
        )

    # Update delivery
    delivery.status = DeliveryStatus.DELIVERED
    delivery.delivery_time = datetime.utcnow()

    # Update donation status
    delivery.donation.status = DonationStatus.DELIVERED

    db.commit()
    db.refresh(delivery)

    return delivery
