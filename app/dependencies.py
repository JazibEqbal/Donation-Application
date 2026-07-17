from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.oauth import oauth2_scheme
from app.core.security import verify_access_token
from app.database import SessionLocal
from app.enums.user import UserRole
from app.models.user import User


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    # Find user
    user = (
        db.query(User)
        .filter(User.id == int(payload["sub"]))
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


def require_role(required_role: UserRole):
    """
    Returns a dependency that allows only users
    with the specified role.
    """

    def role_checker(
        current_user=Depends(get_current_user),
    ):
        # Reject users with a different role
        if current_user.role != required_role:
            raise HTTPException(
                status_code=403,
                detail="You are not authorized to perform this action.",
            )

        return current_user

    return role_checker


def require_not_role(disallowed_role: UserRole):
    """
    Returns a dependency that allows only users
    with the specified role.
    """

    def role_checker(
        current_user=Depends(get_current_user),
    ):
        # Reject users with a different role
        if current_user.role == disallowed_role:
            raise HTTPException(
                status_code=403,
                detail="You are not authorized to perform this action.",
            )

        return current_user

    return role_checker