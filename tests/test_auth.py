from tests.utils import register_user, login_user, _get


def test_register_user(client, donor_data):
    response = register_user(client, donor_data)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["name"] == donor_data["name"]
    assert response_data["email"] == donor_data["email"]
    assert response_data["role"] == donor_data["role"]

    assert "password" not in response_data


def test_register_user_with_existing_email(client, donor_data):
    response = register_user(client, donor_data)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["name"] == donor_data["name"]
    assert response_data["email"] == donor_data["email"]
    assert response_data["role"] == donor_data["role"]

    assert "password" not in response_data

    response = register_user(client, donor_data)

    assert response.status_code == 400

    response = response.json()

    assert response.get('detail') == "Email already registered"


def test_login_user_success(client, donor_data):

    register_user(client, donor_data)

    response = login_user(client, email=donor_data["email"], password=donor_data["password"])

    assert response.status_code == 200


def test_login_user_failure(client, donor_data):
    password= "ffffffff"

    register_user(client, donor_data)

    response = login_user(client, email=donor_data["email"], password=password)

    assert response.status_code == 401

    response = response.json()

    assert response.get('detail') == "Invalid email or password"


def test_get_user_profile(
        client,
        donor_data,
        donor_token
):

    assert donor_token is not None

    response = _get(client, url="/me", token=donor_token)

    response_data = response.json()

    assert response_data["name"] == donor_data["name"]
    assert response_data["email"] == donor_data["email"]
    assert response_data["role"] == donor_data["role"]

    assert "password" not in response_data


def test_get_user_profile_with_invalid_token(
        client,
        donor_data,
        donor_token
):

    assert donor_token is not None

    response = _get(client, url="/me", token=donor_token)

    response_data = response.json()

    assert response_data["name"] == donor_data["name"]
    assert response_data["email"] == donor_data["email"]
    assert response_data["role"] == donor_data["role"]

    assert "password" not in response_data

    response = _get(client, url="/me", token='hfhhhhhhhh444jjjwjwjw')

    assert response.status_code == 401

    response = response.json()

    assert response.get('detail') == "Invalid token"