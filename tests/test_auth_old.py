# def test_register_user(client):
#
#     data = {
#         "name": "tes33t",
#         "password": "test123",
#         "email": "tes33t@email.com",
#         "role": "DONOR"
#     }
#
#     response = client.post(
#         "/register",
#         json=data,
#     )
#
#     assert response.status_code == 200
#
#     response_data = response.json()
#
#     assert response_data["name"] == data["name"]
#     assert response_data["email"] == data["email"]
#     assert response_data["role"] == data["role"]
#
#     assert "password" not in response_data
#
#
# def test_login_user_success(client):
#
#     data = {
#         "name": "tes33t",
#         "password": "test123",
#         "email": "tes33t@email.com",
#         "role": "DONOR"
#     }
#
#     client.post(
#         "/register",
#         json=data,
#     )
#
#     login_data = {
#         "email": data["email"],
#         "password": data["password"]
#     }
#
#     response = client.post(
#         "/login",
#         json=login_data,
#     )
#     client.get(
#         "/me")
#     assert response.status_code == 200
#
#     response_data = response.json()
#
#     assert response_data['token_type'] == "bearer"
#     assert "access_token" in response_data
#
#
# def test_login_user_failure(client):
#     data = {
#         "email": "tes335t@email.com",
#         "password": "ffffffff"
#     }
#
#     response = client.post(
#         "/login",
#         json=data,
#     )
#
#     assert response.status_code == 401
