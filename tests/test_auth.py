"""
Authentication Tests
Verify token creation and validation
"""
import pytest
from utils.api_helpers import create_auth_token


@pytest.mark.auth
@pytest.mark.smoke
def test_create_auth_token_valid_credentials():
    """
    Test authentication with valid credentials
    Expected: Returns valid token string
    """
    token = create_auth_token(username="admin", password="password123")
    
    assert token is not None, "Token should not be None"
    assert isinstance(token, str), "Token should be a string"
    assert len(token) > 0, "Token should not be empty"


@pytest.mark.auth
def test_create_auth_token_invalid_credentials():
    """
    Test authentication with invalid credentials
    Expected: Returns None (no token)
    """
    token = create_auth_token(username="admin", password="wrongpassword")
    
    assert token is None, "Token should be None for invalid credentials"


@pytest.mark.auth
def test_create_auth_token_missing_username():
    """
    Test authentication with missing username
    Expected: Returns None (no token)
    """
    token = create_auth_token(username="", password="password123")
    
    assert token is None, "Token should be None when username is missing"


@pytest.mark.auth
def test_auth_token_fixture(auth_token):
    """
    Test that the auth_token fixture works correctly
    Expected: Fixture provides valid token
    """
    assert auth_token is not None, "Auth token fixture should provide a token"
    assert isinstance(auth_token, str), "Auth token should be a string"
    assert len(auth_token) > 0, "Auth token should not be empty"