from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.auth import (
    LoginRequest,
    Token,
)

router = APIRouter()

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role,
    )

    db.add(new_user)
    db.commit()

    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "role": new_user.role,
    }


@router.post("/login")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        data = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
        }
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
    )


@router.get("/me")
def get_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Return logged-in user's profile.
    """

    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
    }