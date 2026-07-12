from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_role
from app.dependencies import require_not_role
from app.enums.user import UserRole
from app.models.user import User
from app.schemas.requests import (
    RequestCreate,
    RequestResponse,
)
from app.service import request_service

router = APIRouter(
    prefix="/requests",
    tags=["Requests"],
)


@router.post(
    "/",
    response_model=RequestResponse,
)
def create_request(
    request: RequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_not_role(UserRole.DONOR)
    ),
):
    return request_service.create_request(
        db=db,
        request=request,
        requester=current_user,
    )


@router.put(
    "/{request_id}/approve",
    response_model=RequestResponse,
)
def approve_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.DONOR)
    ),
):
    return request_service.approve_request(
        db=db,
        request_id=request_id,
        user=current_user,
    )