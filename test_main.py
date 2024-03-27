import warnings
from fastapi import requests
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

technician_access_token = ""
technician_token_type = ""

admin_access_token = ""
admin_token_type = ""

def test_login_successful():
    # Assuming a valid username and password combination
    global technician_access_token, technician_token_type, admin_access_token, admin_token_type
    response = client.post(
        "/login",
        data={"username": "panindhra", "password": "Panindhra@1234"}
    )
    technician_access_token = response.json()["access_token"]
    technician_token_type = response.json()["token_type"]
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

    response = client.post(
        "/login",
        data={"username": "admin", "password": "Admin@123"}
    )
    admin_access_token = response.json()["access_token"]
    admin_token_type = response.json()["token_type"]
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

def test_get_all_technicians():
    headers = {"accept": "application/json"}
    headers["Authorization"] = f"Bearer {admin_access_token}"

    response = client.get("/technicians/all_technicians", headers=headers)
    assert response.status_code == 200
    assert response.json() is not None

def test_get_all_technicians_wrongtoken():
    headers = {"accept": "application/json"}
    headers["Authorization"] = f"Bearer admin_access_token"

    response = client.get("/technicians/all_technicians", headers=headers)
    assert response.status_code == 401
    assert response.json() is not None

def test_nearest_technician():
    headers = {"accept": "application/json"}
    headers["Authorization"] = f"Bearer {technician_access_token}"

    response = client.get(
        f"/technicians/nearest_technician?lat=12.976818358798672&long=77.72269960072731&skill_set=router%20setup",
        headers=headers
    )
    assert response.status_code == 200
    assert response.json() is not None

def test_nearest_technician_wrongtoken():
    headers = {"accept": "application/json"}
    headers["Authorization"] = f"Bearer technician_access_token"

    response = client.get(
        f"/technicians/nearest_technician?lat=12.976818358798672&long=77.72269960072731&skill_set=router%20setup",
        headers=headers
    )
    assert response.status_code == 401
    assert response.json() is not None


# def test_query_endpoint():
#     headers = {"accept": "application/json"}
#     headers["Authorization"] = f"Bearer {technician_access_token}"

#     response = client.get(
#         "/llm/query?query=I%20need%20help%20in%20installing%20this%20software&lat=12.963463101392353&long=77.7219928645499",
#         headers=headers
#     )

#     assert response.status_code == 200
#     assert response.json() is not None

def test_update_cluster_id_technician():
    headers = {"accept": "application/json"}
    headers["Authorization"] = f"Bearer {admin_access_token}"

    response = client.get("/technicians/update_cluster_id_technician", headers=headers)

    assert response.status_code == 200
    assert response.json() is not None

def test_update_cluster_id_technician_unauthorized():
    headers = {"accept": "application/json"}
    headers["Authorization"] = f"Bearer {technician_access_token}"

    response = client.get("/technicians/update_cluster_id_technician", headers=headers)

    assert response.status_code == 403
    assert response.json()["detail"] == "Permission denied"






# tickets/auto_assign_toggle/{status}

def test_valid_request():
    headers = {'accept': 'application/json', 'Authorization': f'Bearer {admin_access_token}'}
    response = client.get("/tickets/auto_assign_status", headers=headers)
    # self.assertEqual(response.status_code, 200)
    assert response.status_code == 200
def test_missing_token():
    headers = {'accept': 'application/json','Authorization': f'Bearer {admin_access_token}'}
    response = client.get("/tickets/auto_assign_status", headers=headers)
    # self.assertEqual(response.status_code, 401)
    assert response.status_code == 200
        
def test_toggle_auto_assign_true():
    headers = {'accept': 'application/json', 'Authorization': f'Bearer {admin_access_token}'}
    response = client.post("/tickets/auto_assign_toggle/true", headers=headers)
    assert response.status_code == 200

def test_toggle_auto_assign_false():
    headers = {'accept': 'application/json', 'Authorization': f'Bearer {admin_access_token}'}
    response = client.post("/tickets/auto_assign_toggle/false", headers=headers)
    assert response.status_code == 200

def test_missing_token():
    response = client.post("/tickets/auto_assign_toggle/true")
    assert response.status_code == 401

def test_invalid_token():
    headers = {'accept': 'application/json', 'Authorization': 'Bearer invalid_token'}
    response = client.post("/tickets/auto_assign_toggle/true", headers=headers)
    assert response.status_code == 401



#  tickets/create_ticket

# def test_create_ticket_valid():
#     headers = {
#         'accept': 'application/json',
#         'Authorization': f'Bearer {admin_access_token}',
#         'Content-Type': 'application/json'
#     }
#     data = {
#         "title": "router setup",
#         "description": "string",
#         "status": "open",
#         "priority": 1,
#         "location": [12.961591873283192, 77.71770730701556]
#     }
#     response = client.post("/tickets/create_ticket", headers=headers, json=data)
#     assert response.status_code == 200

def test_create_ticket_missing_token():
    data = {
        "title": "router setup",
        "description": "string",
        "status": "open",
        "priority": 1,
        "location": [12.961591873283192, 77.71770730701556]
    }
    response = client.post("/tickets/create_ticket", json=data)
    assert response.status_code == 401

def test_create_ticket_invalid_token():
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer invalid_token',
        'Content-Type': 'application/json'
    }
    data = {
        "title": "router setup",
        "description": "string",
        "status": "open",
        "priority": 1,
        "location": [12.961591873283192, 77.71770730701556]
    }
    response = client.post("/tickets/create_ticket", headers=headers, json=data)
    assert response.status_code == 401

def test_create_ticket_non_admin_access():
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {technician_access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        "title": "router setup",
        "description": "string",
        "status": "open",
        "priority": 1,
        "location": [12.961591873283192, 77.71770730701556]
    }
    response = client.post("/tickets/create_ticket", headers=headers, json=data)
    assert response.status_code == 403


# tickets/all_tickets



def test_get_all_tickets_valid():
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {admin_access_token}'
    }
    response = client.get("/tickets/all_tickets", headers=headers)
    assert response.status_code == 200

def test_get_all_tickets_missing_token():
    response = client.get("/tickets/all_tickets")
    assert response.status_code == 401

def test_get_all_tickets_invalid_token():
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer invalid_token'
    }
    response = client.get("/tickets/all_tickets", headers=headers)
    assert response.status_code == 401

def test_get_all_tickets_non_admin_access():
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {technician_access_token}'
    }
    response = client.get("/tickets/all_tickets", headers=headers)
    assert response.status_code == 403

def test_get_infographics_technicians_valid():
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {admin_access_token}'
    }
    response = client.get("/infographics/get_infographics_technicians", headers=headers)
    assert response.status_code == 200
    assert response.json() is not None

def test_get_infographics_technicians_missing_token():
    response = client.get("/infographics/get_infographics_technicians")
    assert response.status_code == 401

def test_get_infographics_technicians_invalid_token():
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer admin_access_token'
    }
    response = client.get("/infographics/get_infographics_technicians", headers=headers)
    assert response.status_code == 401

def test_get_infographics_technicians_non_admin_access():
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {technician_access_token}'
    }
    response = client.get("/infographics/get_infographics_technicians", headers=headers)
    assert response.status_code == 403
