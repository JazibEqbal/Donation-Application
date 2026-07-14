def register_user(
        client,
        data
):
    return client.post(
        "/register",
        json=data
    )


def login_user(
        client,
        email,
        password
):
    return client.post(
        "/login",
        json={
            "email": email,
            "password": password
        }
    )


def get_current_user(
        client,
        headers
):
    return client.get(
        "/me",
        headers=headers
    )


def get_access_token(
        client,
        email,
        password
):
    response = login_user(
        client,
        email,
        password
    )

    return response.json()["access_token"]


def get_authentication_header(token):
    return {
        "Authorization": f"Bearer {token}"
    }
