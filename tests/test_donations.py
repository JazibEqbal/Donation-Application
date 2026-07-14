from tests.utils import register_user, get_access_token, get_authentication_header, get_current_user


def test_create_donation(
        client,
        donor_data
):
    register_user(client, donor_data)

    token = get_access_token(
        client,
        donor_data['email'],
        donor_data['password'],
    )

    assert token is not None

    headers = get_authentication_header(token)

    assert headers is not None

    # current_user = get_current_user(client, headers)
    # assert current_user is not None
    # data = current_user.json()
    # user_id = data["id"]

    donation_data = {
        "food_name": "Biryani",
        "quantity": 25,
        "category": "MEAL",
        "expiry_time": "2026-12-31T20:00:00",
        "pickup_address": "MG Road, Pune",
        "latitude": 18.5204,
        "longitude": 73.8567,
    }

    # create donation
    response = client.post(
        "/donations",
        json=donation_data,
        headers=headers,
    )

    assert response.status_code == 200
    data = response.json()

    assert data['food_name'] == 'Biryani'
    assert data['quantity'] == 25