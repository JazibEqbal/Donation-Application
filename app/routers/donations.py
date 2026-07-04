from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import require_role, get_db
from app.enums.donation import DonationStatus
from app.enums.user import UserRole
from app.models.donation import Donation
from app.models.user import User
from app.schemas.donation import DonationResponse, DonationCreate

router = APIRouter(
    prefix="/donations",
    tags=["Donations"],
)


@router.post(
    "/",
    response_model=DonationResponse,
)
def create_donation(
    donation: DonationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.DONOR)
    ),
):

    # Create donation object
    new_donation = Donation(
        donor_id=current_user.id,
        food_name=donation.food_name,
        quantity=donation.quantity,
        category=donation.category,
        pickup_address=donation.pickup_address,
        latitude=donation.latitude,
        longitude=donation.longitude,
        expiry_time=donation.expiry_time,
        status=DonationStatus.AVAILABLE,
    )

    # Save to database
    db.add(new_donation)
    db.commit()

    db.refresh(new_donation)

    return new_donation


@router.get(
    "/",
    response_model=list[DonationResponse],
)
def get_all_donations(
    db: Session = Depends(get_db),
):
    # Return all donations
    return db.query(Donation).all()