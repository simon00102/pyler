import pytest
from fastapi import HTTPException
from utils.auth import verify_access_token, verify_admin_role, verify_user_role
import requests

@pytest.fixture(scope="module")
def admin_token():
    response = requests.post("http://localhost:9999/login", json={"username": "pyler", "password": "pyler1!"})
    assert response.status_code == 200
    return response.json().get("access_token")

@pytest.fixture(scope="module")
def user_token():
    response = requests.post("http://localhost:9999/login", json={"username": "simon", "password": "simon"})
    assert response.status_code == 200
    return response.json().get("access_token")

def test_verify_access_token(admin_token:str):
    token_data = verify_access_token(admin_token)
    assert token_data is not None
    assert token_data["username"] == "pyler"
    assert "admin" in token_data["roles"]

def test_verify_access_token_user(user_token:str):
    token_data = verify_access_token(user_token)
    assert token_data is not None
    assert token_data["username"] == "simon"
    assert "user" in token_data["roles"]

def test_verify_admin_role(admin_token:str):
    token_data = verify_access_token(admin_token)
    assert token_data is not None
    username = verify_admin_role(token_data)
    assert username == "pyler"

def test_verify_admin_role_unauthorized(user_token:str):
    token_data = verify_access_token(user_token)
    assert token_data is not None

    with pytest.raises(HTTPException) as excinfo:
        verify_admin_role(token_data)
    assert excinfo.value.status_code == 403

def test_verify_user_role(user_token:str):
    token_data = verify_access_token(user_token)
    assert token_data is not None
    username = verify_user_role(token_data)
    assert username == "simon"

def test_verify_user_role_admin(admin_token:str):
    token_data = verify_access_token(admin_token)
    assert token_data is not None
    username = verify_user_role(token_data)
    assert username == "pyler"
