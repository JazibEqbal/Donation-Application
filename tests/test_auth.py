from tests.conftest import donor_data
from tests.utils import register_user, get_access_token, get_authentication_header


def test_register_user(client, donor_data):

    response = register_user(client, donor_data)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["name"] == donor_data["name"]
    assert response_data["email"] == donor_data["email"]
    assert response_data["role"] == donor_data["role"]

    assert "password" not in response_data


def test_login_user_success(client, donor_data):

    register_user(
        client,
        donor_data
    )

    token = get_access_token(
        client,
        donor_data['email'],
        donor_data['password'],
    )

    assert token is not None


def test_login_user_failure(client):
    data = {
        "email": "tes335t@email.com",
        "password": "ffffffff"
    }

    response = client.post(
        "/login",
        json=data,
    )

    assert response.status_code == 401

def test_get_user_profile(
        client,
        donor_data
):

    register_user(
        client,
        donor_data
    )

    token = get_access_token(
        client,
        donor_data['email'],
        donor_data['password'],
    )

    assert token is not None

    headers = get_authentication_header(token)

    response = client.get(
        "/me",
        headers=headers
    )

    response_data = response.json()

    assert response_data["name"] == donor_data["name"]
    assert response_data["email"] == donor_data["email"]
    assert response_data["role"] == donor_data["role"]

    assert "password" not in response_data