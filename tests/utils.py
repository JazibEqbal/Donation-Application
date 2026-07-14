def create_user_data(
    name: str,
    email: str,
    role: str,
):
    # Create sample user data
    return {
        "name": name,
        "email": email,
        "password": "Password123",
        "role": role,
    }


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


def _get(client, url, token, **kwargs):
    return client.get(
        url,
        headers=get_authentication_header(token),
        **kwargs,
    )


def _post(client, url, token, **kwargs):
    return client.post(
        url,
        headers=get_authentication_header(token),
        **kwargs,
    )


def _put(client, url, token, **kwargs):
    return client.put(
        url,
        headers=get_authentication_header(token),
        **kwargs,
    )


def _delete(client, url, token, **kwargs):
    return client.delete(
        url,
        headers=get_authentication_header(token),
        **kwargs,
    )
