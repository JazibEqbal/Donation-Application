from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_role
from app.enums.user import UserRole
from app.models.user import User
from app.schemas.delivery import DeliveryResponse
from app.services import delivery_service

router = APIRouter(
    prefix="/deliveries",
    tags=["Deliveries"],
)


@router.put(
    "/{delivery_id}/accept",
    response_model=DeliveryResponse,
)
def accept_delivery(
    delivery_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.VOLUNTEER)
    ),
):
    return delivery_service.accept_delivery(
        db=db,
        delivery_id=delivery_id,
        volunteer=current_user,
    )


@router.put(
    "/{delivery_id}/pickup",
    response_model=DeliveryResponse,
)
def pickup_delivery(
    delivery_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.VOLUNTEER)
    ),
):
    return delivery_service.pickup_delivery(
        db=db,
        delivery_id=delivery_id,
        volunteer=current_user,
    )


@router.put(
    "/{delivery_id}/delivered",
    response_model=DeliveryResponse,
)
def mark_delivered(
    delivery_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.VOLUNTEER)
    ),
):
    return delivery_service.mark_delivered(
        db=db,
        delivery_id=delivery_id,
        volunteer=current_user,
    )
