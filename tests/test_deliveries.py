from tests.utils import _post, login_user, _put, register_user, create_user_data


def test_accept_delivery(
        client, 
        donor_token, 
        ngo_token, 
        volunteer_token, 
        donor_data
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
    delivery_id = data.get('id')

    assert ngo_token is not None

    # user creates a request to get the donation
    response = _post(client, url="/requests", token=ngo_token, json={
        "donation_id": delivery_id,
    })

    assert response.status_code == 200

    data = response.json()

    request_id = data.get('id')

    # donor logins and approves the requested donation
    response = login_user(client, email=donor_data["email"], password=donor_data["password"])

    assert response.status_code == 200

    # get donor token
    data = response.json()

    response = _put(client, url=f"/requests/{request_id}/approve", token=data["access_token"])

    assert response.status_code == 200

    # volunteer accepts the delivery
    response = _put(client, url=f"/deliveries/{delivery_id}/accept", token=volunteer_token)

    assert response.status_code == 200


def test_accept_delivery_only_by_volunteer(
        client, 
        donor_token, 
        ngo_token, 
        volunteer_token, 
        donor_data
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
    delivery_id = data.get('id')

    assert ngo_token is not None

    # user creates a request to get the donation
    response = _post(client, url="/requests", token=ngo_token, json={
        "donation_id": delivery_id,
    })

    assert response.status_code == 200

    data = response.json()

    request_id = data.get('id')

    # donor logins and approves the requested donation
    response = login_user(client, email=donor_data["email"], password=donor_data["password"])

    assert response.status_code == 200

    # get donor token
    data = response.json()

    response = _put(client, url=f"/requests/{request_id}/approve", token=data["access_token"])

    assert response.status_code == 200

    # ngo tries to accept the delivery
    response = _put(client, url=f"/deliveries/{delivery_id}/accept", token=ngo_token)

    assert response.status_code == 403

    response = response.json()

    assert response.get('detail') == "You are not authorized to perform this action."
    
    
def test_accept_delivery_only_if_delivery_is_not_assigned_to_any_volunteer(
        client, 
        donor_token, 
        ngo_token, 
        volunteer_token, 
        donor_data
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
    delivery_id = data.get('id')

    assert ngo_token is not None

    # user creates a request to get the donation
    response = _post(client, url="/requests", token=ngo_token, json={
        "donation_id": delivery_id,
    })

    assert response.status_code == 200

    data = response.json()

    request_id = data.get('id')

    # donor logins and approves the requested donation
    response = login_user(client, email=donor_data["email"], password=donor_data["password"])

    assert response.status_code == 200

    # get donor token
    data = response.json()

    response = _put(client, url=f"/requests/{request_id}/approve", token=data["access_token"])

    assert response.status_code == 200

    # volunteer 1 accepts the delivery
    response = _put(client, url=f"/deliveries/{delivery_id}/accept", token=volunteer_token)

    assert response.status_code == 200
    
    # create volunteer x
    volunteer_x =  create_user_data(
        "Volunteer",
        "volunteerX@test.com",
        "VOLUNTEER",
    )

    register_user(client=client, data=volunteer_x)

    # volunteer x logins
    response = login_user(client, email=volunteer_x["email"], password=volunteer_x["password"])

    assert response.status_code == 200

    volunteer_x_data = response.json()

    # volunteer x tries to accept the delivery
    response = _put(client, url=f"/deliveries/{delivery_id}/accept", token=volunteer_x_data["access_token"])

    assert response.status_code == 400

    response = response.json()

    assert response.get('detail') == "Delivery already assigned"


def test_pickup_delivery(
        client,
        donor_token,
        ngo_token,
        volunteer_token,
        donor_data
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
    delivery_id = data.get('id')

    assert ngo_token is not None

    # user creates a request to get the donation
    response = _post(client, url="/requests", token=ngo_token, json={
        "donation_id": delivery_id,
    })

    assert response.status_code == 200

    data = response.json()

    request_id = data.get('id')

    # donor logins and approves the requested donation
    response = login_user(client, email=donor_data["email"], password=donor_data["password"])

    assert response.status_code == 200

    # get donor token
    data = response.json()

    response = _put(client, url=f"/requests/{request_id}/approve", token=data["access_token"])

    assert response.status_code == 200

    # volunteer accepts the delivery
    response = _put(client, url=f"/deliveries/{delivery_id}/accept", token=volunteer_token)

    assert response.status_code == 200

    # volunteer pickup the delivery
    response = _put(client, url=f"/deliveries/{delivery_id}/pickup", token=volunteer_token)

    assert response.status_code == 200


def test_pickup_delivery_again(
        client,
        donor_token,
        ngo_token,
        volunteer_token,
        donor_data,
        volunteer_data
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
    delivery_id = data.get('id')

    assert ngo_token is not None

    # user creates a request to get the donation
    response = _post(client, url="/requests", token=ngo_token, json={
        "donation_id": delivery_id,
    })

    assert response.status_code == 200

    data = response.json()

    request_id = data.get('id')

    # donor logins and approves the requested donation
    response = login_user(client, email=donor_data["email"], password=donor_data["password"])

    assert response.status_code == 200

    # get donor token
    data = response.json()

    response = _put(client, url=f"/requests/{request_id}/approve", token=data["access_token"])

    assert response.status_code == 200

    # volunteer accepts the delivery
    response = _put(client, url=f"/deliveries/{delivery_id}/accept", token=volunteer_token)

    assert response.status_code == 200

    # volunteer pickup the delivery 1st time
    response = _put(client, url=f"/deliveries/{delivery_id}/pickup", token=volunteer_token)

    assert response.status_code == 200

    # volunteer tries to pick up the delivery for the 2nd time
    response = _put(client, url=f"/deliveries/{delivery_id}/pickup", token=volunteer_token)

    assert response.status_code == 400

    response = response.json()

    assert response.get('detail') ==  "Delivery already picked up"


def test_delivery_pickup_only_by_volunteer_who_has_been_assigned(
        client,
        donor_token,
        ngo_token,
        volunteer_token,
        donor_data
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
    delivery_id = data.get('id')

    assert ngo_token is not None

    # user creates a request to get the donation
    response = _post(client, url="/requests", token=ngo_token, json={
        "donation_id": delivery_id,
    })

    assert response.status_code == 200

    data = response.json()

    request_id = data.get('id')

    # donor logins and approves the requested donation
    response = login_user(client, email=donor_data["email"], password=donor_data["password"])

    assert response.status_code == 200

    # get donor token
    data = response.json()

    response = _put(client, url=f"/requests/{request_id}/approve", token=data["access_token"])

    assert response.status_code == 200

    # volunteer 1 accepts the delivery
    response = _put(client, url=f"/deliveries/{delivery_id}/accept", token=volunteer_token)

    assert response.status_code == 200

    # create volunteer x
    volunteer_x = create_user_data(
        "Volunteer",
        "volunteerX@test.com",
        "VOLUNTEER",
    )

    register_user(client=client, data=volunteer_x)

    # volunteer x logins
    response = login_user(client, email=volunteer_x["email"], password=volunteer_x["password"])

    assert response.status_code == 200

    volunteer_x_data = response.json()

    # volunteer x tries to pick up the delivery to whom delivery is not assigned
    response = _put(client, url=f"/deliveries/{delivery_id}/pickup", token=volunteer_x_data["access_token"])

    assert response.status_code == 403

    response = response.json()

    assert response.get('detail') == "You are not assigned to this delivery"


def test_mark_delivered(
        client,
        donor_token,
        ngo_token,
        volunteer_token,
        donor_data
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
    delivery_id = data.get('id')

    assert ngo_token is not None

    # user creates a request to get the donation
    response = _post(client, url="/requests", token=ngo_token, json={
        "donation_id": delivery_id,
    })

    assert response.status_code == 200

    data = response.json()

    request_id = data.get('id')

    # donor logins and approves the requested donation
    response = login_user(client, email=donor_data["email"], password=donor_data["password"])

    assert response.status_code == 200

    # get donor token
    data = response.json()

    response = _put(client, url=f"/requests/{request_id}/approve", token=data["access_token"])

    assert response.status_code == 200

    # volunteer accepts the delivery
    response = _put(client, url=f"/deliveries/{delivery_id}/accept", token=volunteer_token)

    assert response.status_code == 200

    # volunteer pickups the delivery
    response = _put(client, url=f"/deliveries/{delivery_id}/pickup", token=volunteer_token)

    assert response.status_code == 200

    # volunteer marks the delivery as delivered
    response = _put(client, url=f"/deliveries/{delivery_id}/delivered", token=volunteer_token)

    assert response.status_code == 200


def test_delivery_marked_only_by_volunteer_who_has_been_assigned(
        client,
        donor_token,
        ngo_token,
        volunteer_token,
        donor_data
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
    delivery_id = data.get('id')

    assert ngo_token is not None

    # user creates a request to get the donation
    response = _post(client, url="/requests", token=ngo_token, json={
        "donation_id": delivery_id,
    })

    assert response.status_code == 200

    data = response.json()

    request_id = data.get('id')

    # donor logins and approves the requested donation
    response = login_user(client, email=donor_data["email"], password=donor_data["password"])

    assert response.status_code == 200

    # get donor token
    data = response.json()

    response = _put(client, url=f"/requests/{request_id}/approve", token=data["access_token"])

    assert response.status_code == 200

    # volunteer 1 accepts the delivery
    response = _put(client, url=f"/deliveries/{delivery_id}/accept", token=volunteer_token)

    assert response.status_code == 200

    # create volunteer x
    volunteer_x = create_user_data(
        "Volunteer",
        "volunteerX@test.com",
        "VOLUNTEER",
    )

    register_user(client=client, data=volunteer_x)

    # volunteer x logins
    response = login_user(client, email=volunteer_x["email"], password=volunteer_x["password"])

    assert response.status_code == 200

    volunteer_x_data = response.json()

    # volunteer x tries to mark the delivery as delivered to whom the delivery is not assigned
    response = _put(client, url=f"/deliveries/{delivery_id}/delivered", token=volunteer_x_data["access_token"])

    assert response.status_code == 403

    response = response.json()

    assert response.get('detail') == "You are not assigned to this delivery"


def test_delivery_marked_only_by_when_delivery_has_been_picked_up(
        client,
        donor_token,
        ngo_token,
        volunteer_token,
        donor_data
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
    delivery_id = data.get('id')

    assert ngo_token is not None

    # user creates a request to get the donation
    response = _post(client, url="/requests", token=ngo_token, json={
        "donation_id": delivery_id,
    })

    assert response.status_code == 200

    data = response.json()

    request_id = data.get('id')

    # donor logins and approves the requested donation
    response = login_user(client, email=donor_data["email"], password=donor_data["password"])

    assert response.status_code == 200

    # get donor token
    data = response.json()

    response = _put(client, url=f"/requests/{request_id}/approve", token=data["access_token"])

    assert response.status_code == 200

    # volunteer 1 accepts the delivery
    response = _put(client, url=f"/deliveries/{delivery_id}/accept", token=volunteer_token)

    assert response.status_code == 200

    # volunteer tries to mark the delivery as delivered without picking it up
    response = _put(client, url=f"/deliveries/{delivery_id}/delivered", token=volunteer_token)

    assert response.status_code == 400

    response = response.json()

    assert response.get('detail') == "Delivery has not been picked up yet"