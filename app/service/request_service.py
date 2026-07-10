from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.enums.donation import DonationStatus
from app.enums.request import RequestStatus
from app.models.donation import Donation
from app.models.request import DonationRequest
from app.models.user import User
from app.schemas.requests import RequestCreate


def create_request(
        db: Session,
        request: RequestCreate,
        requester: User
) -> DonationRequest:

    # Find donation
    donation = (
        db.query(Donation)
        .filter(Donation.id == request.donation_id)
        .first()
    )

    # check if donation exist
    if donation is None:
        raise HTTPException(
            status_code=404,
            detail="Donation not found",
        )

    # check if donation is available
    if donation.status != DonationStatus.AVAILABLE:
        raise HTTPException(
            status_code=400,
            detail="Donation is not available",
        )

    # confirm if requester cannot request their own donation
    if requester.id == donation.donor_id:
        raise HTTPException(
            status_code=400,
            detail="You cannot request your own donation",
        )

    # Prevent duplicate request
    existing_request = (
        db.query(DonationRequest)
        .filter(
            DonationRequest.donation_id == donation.id,
            DonationRequest.requester_id == requester.id,
        )
        .first()
    )

    if existing_request:
        raise HTTPException(
            status_code=400,
            detail="You have already requested this donation",
        )

    # create request
    new_request = DonationRequest(
        donation_id = donation.donor_id,
        requester_id = requester.id,
        status = RequestStatus.PENDING
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return new_request
