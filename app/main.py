from fastapi import FastAPI
from app.database import Base
from app.database import engine
from app.routers.auth import router as auth_router
from app.routers.donations import router as donation_router
from app.routers.requests import router as request_router
from app.models.donation import Donation
from app.models.user import User
from app.models.request import DonationRequest


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Donation Platform"
)

app.include_router(auth_router)
app.include_router(donation_router)
app.include_router(request_router)


@app.get("/")
def home():
    return {
        "message": "Donation Platform"
    }
