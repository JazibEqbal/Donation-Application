from sqlalchemy.orm import Session

from app.enums.donation import DonationStatus
from app.models.donation import Donation
from app.models.user import User
from app.schemas.donation import DonationCreate


def create_donation(
    db: Session,
    donation: DonationCreate,
    donor: User,
) -> Donation:
    """
    Create a new donation for the logged-in donor.
    """
    new_donation = Donation(
        **donation.model_dump(),
        donor_id=donor.id,
        status=DonationStatus.AVAILABLE,
    )

    db.add(new_donation)
    db.commit()
    db.refresh(new_donation)

    return new_donation


def get_all_donations(
    db: Session,
) -> list[type[Donation]]:
    """
    Return all donations.
    """

    return db.query(Donation).all()
