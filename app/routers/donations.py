from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import require_role, get_db
from app.enums.donation import DonationStatus
from app.enums.user import UserRole
from app.models.donation import Donation
from app.models.user import User
from app.schemas.donation import DonationResponse, DonationCreate
from app.service import donation_service

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

    return donation_service.create_donation(
        db=db,
        donation=donation,
        donor=current_user,
    )


@router.get(
    "/",
    response_model=list[DonationResponse],
)
def get_all_donations(
    db: Session = Depends(get_db),
):
    # Fetch all donations
    return donation_service.get_all_donations(db)
