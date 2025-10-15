
"""
Pytest Configuration and Fixtures
Shared setup code that runs before tests
"""
import pytest
from utils.api_helpers import create_auth_token, create_booking


@pytest.fixture(scope="session")
def auth_token():
    """
    Create authentication token once for entire test session
    This runs once and is shared by all tests that need it
    """
    token = create_auth_token()
    assert token is not None, "Failed to create auth token"
    return token


@pytest.fixture(scope="function")
def new_booking():
    """
    Create a fresh booking for each test that needs one
    This runs before each test function that uses it
    Returns the booking ID and full response data
    """
    response = create_booking(
        firstname="Test",
        lastname="User",
        totalprice=150,
        depositpaid=True,
        checkin="2025-11-01",
        checkout="2025-11-05",
        additionalneeds="Breakfast"
    )
    
    assert response.status_code == 200, f"Failed to create booking: {response.status_code}"
    
    data = response.json()
    booking_id = data.get("bookingid")
    booking_data = data.get("booking")
    
    return {
        "id": booking_id,
        "data": booking_data
    }