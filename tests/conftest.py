import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.dependencies import get_db
from app.main import app
from tests.utils import create_user_data, register_user, get_access_token


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

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

# ------ CLIENT FIXTURE --> sends HTTP requests
@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


# ------ *DATA FIXTURES --> define user payloads
@pytest.fixture
def donor_data():
    return create_user_data(
        "Donor",
        "donor@test.com",
        "DONOR",
    )


@pytest.fixture
def ngo_data():
    return create_user_data(
        "NGO",
        "ngo@test.com",
        "NGO",
    )


@pytest.fixture
def admin_data():
    return create_user_data(
        "Admin",
        "admin@test.com",
        "ADMIN",
    )


@pytest.fixture
def volunteer_data():
    return create_user_data(
        "Volunteer",
        "volunteer@test.com",
        "VOLUNTEER",
    )


# ------ *TOKEN FIXTURES --> create users and return authentication tokens
@pytest.fixture
def donor_token(client, donor_data):
    register_user(client, donor_data)

    return get_access_token(
        client,
        donor_data["email"],
        donor_data["password"],
    )


@pytest.fixture
def ngo_token(client, ngo_data):
    register_user(client, ngo_data)

    return get_access_token(
        client,
        ngo_data["email"],
        ngo_data["password"],
    )


@pytest.fixture
def admin_token(client, admin_data):
    register_user(client, admin_data)

    return get_access_token(
        client,
        admin_data["email"],
        admin_data["password"],
    )


@pytest.fixture
def volunteer_token(client, volunteer_data):
    register_user(client, volunteer_data)

    return get_access_token(
        client,
        volunteer_data["email"],
        volunteer_data["password"],
    )
