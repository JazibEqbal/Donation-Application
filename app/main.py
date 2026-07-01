from fastapi import FastAPI
from app.database import Base
from app.database import engine
from app.routers.auth import router as auth_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Food Waste Donation Platform"
)

app.include_router(auth_router)


@app.get("/")
def home():
    return {
        "message": "Food Waste Donation Platform"
    }