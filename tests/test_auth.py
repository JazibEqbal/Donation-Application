from tests.utils import register_user, get_access_token, get_authentication_header, login_user, _get


def test_register_user(client, donor_data):
    response = register_user(client, donor_data)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["name"] == donor_data["name"]
    assert response_data["email"] == donor_data["email"]
    assert response_data["role"] == donor_data["role"]

    assert "password" not in response_data


def test_login_user_success(client, donor_token):

    token = donor_token

    assert token is not None


def test_login_user_failure(client, donor_data):
    password= "ffffffff"

    register_user(client, donor_data)

    response = login_user(client, email=donor_data["email"], password=password)

    assert response.status_code == 401


def test_get_user_profile(
        client,
        donor_data,
        donor_token
):
    token = donor_token

    assert token is not None

    response = _get(client, url="/me", token=token)

    response_data = response.json()

    assert response_data["name"] == donor_data["name"]
    assert response_data["email"] == donor_data["email"]
    assert response_data["role"] == donor_data["role"]

    assert "password" not in response_data
