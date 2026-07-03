from fastapi import APIRouter, Depends

from app.dependencies import require_role
from app.enums.user import UserRole
from app.models.user import User

router = APIRouter(
    prefix="/donations",
    tags=["Donations"],
)


@router.post("/")
def create_donation(
    current_user: User = Depends(
        require_role(UserRole.DONOR)
    ),
):
    return {
        "message": "Donation creation coming next",
        "donor": current_user.name,
    }