from tests.utils import _post, login_user, _put, create_user_data, register_user


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

    # donor creates a donation
    response = _post(client, url="/donations", token=donor_token, json=donation_data)

    assert response.status_code == 200
    data = response.json()

    # get donation id
    donation_id = data.get('id')

    assert ngo_token is not None

    # user creates a request to get the donation
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

    # donor creates a request to get the donation for themselves
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

    # donor creates a donation
    response = _post(client, url="/donations", token=donor_token, json=donation_data)

    assert response.status_code == 200
    data = response.json()

    # get donation id
    donation_id = data.get('id')

    assert ngo_token is not None

    # user creates a request to get the donation
    response = _post(client, url="/requests", token=ngo_token, json={
        "donation_id": donation_id,
    })

    assert response.status_code == 200

    # the same user tries to create request for the same donation again
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

    # user tries to create a request for the donation which is not available
    response = _post(client, url="/requests", token=ngo_token, json={
        "donation_id": donation_id,
    })

    assert response.status_code == 404

    response = response.json()

    assert response.get('detail') == "Donation not found"


def test_approve_request(
        client,
        donor_token,
        ngo_token,
        donor_data
):

    donation_data = {
        "food_name": "Biryani",
        "quantity": 25,
        "category": "MEAL",
        "expiry_time": "2026-12-31T20:00:00",
        "pickup_address": "MG Road, Pune",
        "latitude": 18.5204,
        "longitude": 73.8567,
    }

    # donation create
    response = _post(client, url="/donations", token=donor_token, json=donation_data)

    assert response.status_code == 200
    data = response.json()

    # get donation id
    donation_id = data.get('id')

    assert ngo_token is not None

    # ngo requests a donation
    response = _post(client, url="/requests", token=ngo_token, json={
        "donation_id": donation_id,
    })

    assert response.status_code == 200

    data = response.json()

    request_id = data.get('id')

    # donor logins
    response = login_user(client, email=donor_data["email"], password=donor_data["password"])

    assert response.status_code == 200

    # get donor token
    data = response.json()

    # donor approves the requested donation
    response = _put(client, url=f"/requests/{request_id}/approve", token=data["access_token"])

    assert response.status_code == 200


def test_approve_request_only_by_whom_donation_is_created(
        client,
        donor_token,
        ngo_token,
        donor_data
):

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

    # get donation id
    donation_id = data.get('id')

    assert ngo_token is not None

    # ngo requests a donation
    response = _post(client, url="/requests", token=ngo_token, json={
        "donation_id": donation_id,
    })

    assert response.status_code == 200

    data = response.json()

    request_id = data.get('id')

    donor_x =  create_user_data(
        "DonorX",
        "donorX@test.com",
        "DONOR",
    )

    register_user(client=client, data=donor_x)

    # any other donor x logins
    response = login_user(client, email=donor_x["email"], password=donor_x["password"])

    assert response.status_code == 200

    # get donor token
    donor_data = response.json()

    # donor x tries to approve the requested donation
    response = _put(client, url=f"/requests/{request_id}/approve", token=donor_data["access_token"])

    assert response.status_code == 403

    response = response.json()

    assert response.get('detail') == "You can approve only your own donations"


def test_approve_request_not_found(
        client,
        donor_token
):
    # donor tries to approve the request which is not available
    response = _put(client, url=f"/requests/{2}/approve", token=donor_token)

    assert response.status_code == 404

    response = response.json()

    assert response.get('detail') == "Request not found"