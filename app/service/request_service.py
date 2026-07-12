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


def approve_request(
        db: Session,
        request_id: int,
        user: User
):
    # find request
    request = (
        db.query(DonationRequest)
        .filter(DonationRequest.id == request_id)
        .first()
    )

    if request is None:
        raise HTTPException(
            status_code=404,
            detail="Request not found",
        )

    # get the related donation
    donation = request.donation

    # a request can be approved only be the creator i.e, donor
    if user.id != donation.donor_id:
        raise HTTPException(
            status_code=403,
            detail="You can approve only your own donations",
        )

    # confirm is donation is still available
    if donation.status != DonationStatus.AVAILABLE:
        raise HTTPException(
            status_code=400,
            detail="Donation is no longer available",
        )

    # finally approve requested donation
    request.status = RequestStatus.APPROVED

    # update donation status
    donation.status = DonationStatus.APPROVED

    # once a request is approved, all other request should be rejected
    (
        db.query(DonationRequest)
        .filter(
            DonationRequest.donation_id == donation.id,
            DonationRequest.id != request.id,
            DonationRequest.status == RequestStatus.PENDING,
        )
        .update(
            {
                DonationRequest.status: RequestStatus.REJECTED
            },
            synchronize_session=False,
        )
    )

    db.commit()
    db.refresh(request)

    return request