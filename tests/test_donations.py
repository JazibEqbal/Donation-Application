from tests.utils import _post


def test_create_donation(
        client,
        donor_token
):

    assert donor_token is not None

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
    response = _post(client, url="/donations", token=donor_token, json=donation_data)

    assert response.status_code == 200
    data = response.json()

    assert data['food_name'] == 'Biryani'
    assert data['quantity'] == 25


def test_get_donations(
        client
):
    res = client.get("/donations")

    assert res.status_code == 200


def test_create_donation_without_login(client):
    donation_data = {
        "food_name": "Rice",
        "quantity": 10,
        "category": "MEAL",
        "expiry_time": "2026-12-31T20:00:00",
        "pickup_address": "Pune",
        "latitude": 18.5204,
        "longitude": 73.8567,
    }

    response = client.post(
        "/donations",
        json=donation_data,
    )

    assert response.status_code == 401


def test_create_donation_only_by_donor(
        client,
        ngo_data,
        ngo_token
):

    assert ngo_token is not None

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
    response = _post(
        client,
        url="/donations",
        token=ngo_token,
        json=donation_data
    )

    assert response.status_code == 403