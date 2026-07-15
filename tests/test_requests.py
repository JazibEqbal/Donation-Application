from tests.utils import _post


def test_create_request(
        client,
        donor_token,
        ngo_token
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

    # get donation id
    donation_id = data.get('id')

    assert ngo_token is not None

    # create request
    response = _post(client, url="/requests", token=ngo_token, json={
        "donation_id": donation_id,
    })

    assert response.status_code == 200


def test_create_request_by_self(
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

    response = _post(client, url="/donations", token=donor_token, json=donation_data)

    assert response.status_code == 200
    data = response.json()

    donation_id = data.get('id')

    # create request with the same user
    response = _post(client, url="/requests", token=donor_token, json={
        "donation_id": donation_id,
    })

    assert response.status_code == 403


def test_create_request_already_requested(
        client,
        donor_token,
        ngo_token
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

    # get donation id
    donation_id = data.get('id')

    assert ngo_token is not None

    # create request
    response = _post(client, url="/requests", token=ngo_token, json={
        "donation_id": donation_id,
    })

    assert response.status_code == 200

    # try to create request for the donation which user has already requested
    response = _post(client, url="/requests", token=ngo_token, json={
        "donation_id": donation_id,
    })

    assert response.status_code == 400

    response = response.json()

    assert response.get('detail') == "You have already requested this donation"


def test_create_request_donation_not_found(
        client,
        donor_token,
        ngo_token
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

    response = _post(client, url="/donations", token=donor_token, json=donation_data)

    assert response.status_code == 200
    data = response.json()

    donation_id = 3 # any random donation

    assert ngo_token is not None

    # try to create request
    response = _post(client, url="/requests", token=ngo_token, json={
        "donation_id": donation_id,
    })

    assert response.status_code == 404

    response = response.json()

    assert response.get('detail') == "Donation not found"