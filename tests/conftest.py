import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.dependencies import get_db
from app.database import Base
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Override get_db dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def client():
    # Create fresh database
    Base.metadata.create_all(bind=engine)

    # Override database dependency
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

    if os.path.exists("test.db"):
        os.remove("test.db")


@pytest.fixture
def donor_data():
    # Sample donor data
    return {
        "name": "Test Donor",
        "email": "donor@test.com",
        "password": "Password123",
        "role": "DONOR",
    }