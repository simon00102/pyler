from typing import Any
import pytest
from datetime import timedelta
from fastapi import HTTPException
import jwt
from auth import (
    verify_password,
    get_password_hash,
    create_token,
    verify_admin_access_token,
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

def test_verify_password():
    """Test that password verification works correctly."""
    password = "testpassword"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password) is True
    assert verify_password("wrongpassword", hashed_password) is False

def test_create_token():
    """Test token creation with expiration."""
    data: dict[Any,Any] = {"sub": "testuser", "roles": ["user"]}
    token = create_token(data, timedelta(minutes=5))
    assert isinstance(token, str)

    decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore
    assert decoded_data["sub"] == "testuser"
    assert decoded_data["roles"] == ["user"]


def test_verify_admin_access_token_valid_token():
    """Test that a valid admin access token is accepted."""
    admin_token = create_token(
        {"sub": "adminuser", "roles": ["admin"]},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    username = verify_admin_access_token(admin_token)
    assert username == "adminuser"

def test_verify_admin_access_token_invalid_token():
    """Test that an invalid token raises an HTTP 401 Unauthorized error."""
    with pytest.raises(HTTPException) as exc_info:
        verify_admin_access_token("invalid_token")
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid token"

def test_verify_admin_access_token_expired_token():
    """Test that an expired token raises an HTTP 401 Unauthorized error."""
    expired_token = create_token(
        {"sub": "adminuser", "roles": ["admin"]},
        timedelta(minutes=-1),  # Expired token
    )
    with pytest.raises(HTTPException) as exc_info:
        verify_admin_access_token(expired_token)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Token has expired"

def test_verify_admin_access_token_no_admin_role():
    """Test that a token without the admin role raises an HTTP 403 Forbidden error."""
    user_token = create_token(
        {"sub": "testuser", "roles": ["user"]},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    with pytest.raises(HTTPException) as exc_info:
        verify_admin_access_token(user_token)
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Not enough permissions"
