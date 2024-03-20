from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

access_token = ""
token_type = ""

def test_login_successful():
    # Assuming a valid username and password combination
    global access_token, token_type
    response = client.post(
        "/login",
        data={"username": "panindhra", "password": "Panindhra@1234"}
    )
    access_token = response.json()["access_token"]
    token_type = response.json()["token_type"]

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_user_not_found():
    # Assuming the provided username doesn't exist in the database
    response = client.post(
        "/login",
        data={"username": "non_existing_username", "password": "valid_password"}
    )
    assert response.status_code == 404

def test_login_invalid_credentials():
    # Assuming the username exists but the password is incorrect
    response = client.post(
        "/login",
        data={"username": "panindhra", "password": "invalid_password"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Wrong Username or password"

def test_login_missing_fields():
    # Assuming username and/or password fields are missing
    response = client.post("/login", data={})
    assert response.status_code == 422

def test_login_invalid_payload():
    # Assuming the payload format is incorrect
    response = client.post("/login", json={"user": "username", "pass": "password"})
    assert response.status_code == 422