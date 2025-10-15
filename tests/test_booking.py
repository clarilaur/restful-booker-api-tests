"""
Booking CRUD Tests
Test all Create, Read, Update, Delete operations
"""
import pytest
from utils.api_helpers import (
    get_all_bookings,
    get_booking_by_id,
    create_booking,
    update_booking,
    partial_update_booking,
    delete_booking
)




@pytest.mark.crud
@pytest.mark.smoke
def test_get_all_bookings():
    """
    Test retrieving all booking IDs
    Expected: 200 status, returns array of bookings
    """
    response = get_all_bookings()
    
    assert response.status_code == 200, \
        f"Expected status 200, got {response.status_code}"
    
    data = response.json()
    assert isinstance(data, list), "Response should be a list"
    assert len(data) > 0, "Should have at least one booking"
    assert "bookingid" in data[0], "Each booking should have bookingid"


@pytest.mark.crud
def test_get_booking_by_id(new_booking):
    """
    Test retrieving specific booking by ID
    Expected: 200 status, returns booking details
    """
    booking_id = new_booking["id"]
    response = get_booking_by_id(booking_id)
    
    assert response.status_code == 200, \
        f"Expected status 200, got {response.status_code}"
    
    data = response.json()
    assert "firstname" in data, "Booking should have firstname"
    assert "lastname" in data, "Booking should have lastname"
    assert "totalprice" in data, "Booking should have totalprice"
    assert "bookingdates" in data, "Booking should have bookingdates"


@pytest.mark.crud
def test_get_nonexistent_booking():
    """
    Test retrieving booking that doesn't exist
    Expected: 404 status
    """
    response = get_booking_by_id(999999999)
    
    assert response.status_code == 404, \
        f"Expected status 404 for nonexistent booking, got {response.status_code}"



@pytest.mark.crud
@pytest.mark.smoke
def test_create_booking_success():
    """
    Test creating a new booking
    Expected: 200 status, returns booking with ID
    """
    response = create_booking(
        firstname="Jane",
        lastname="Doe",
        totalprice=250,
        depositpaid=True,
        checkin="2025-12-01",
        checkout="2025-12-05",
        additionalneeds="WiFi"
    )
    
    assert response.status_code == 200, \
        f"Expected status 200, got {response.status_code}"
    
    data = response.json()
    assert "bookingid" in data, "Response should contain bookingid"
    assert "booking" in data, "Response should contain booking data"
    
    booking = data["booking"]
    assert booking["firstname"] == "Jane", "Firstname should match"
    assert booking["lastname"] == "Doe", "Lastname should match"
    assert booking["totalprice"] == 250, "Total price should match"
    assert booking["depositpaid"] is True, "Deposit paid should be True"


@pytest.mark.crud
def test_create_booking_validates_data():
    """
    Test that created booking contains all expected fields
    Expected: All fields present and correct types
    """
    response = create_booking(
        firstname="John",
        lastname="Smith",
        totalprice=100,
        depositpaid=False,
        checkin="2025-11-10",
        checkout="2025-11-15",
        additionalneeds="Parking"
    )
    
    data = response.json()
    booking = data["booking"]
    
 
    assert isinstance(booking["firstname"], str), "Firstname should be string"
    assert isinstance(booking["totalprice"], int), "Totalprice should be integer"
    assert isinstance(booking["depositpaid"], bool), "Depositpaid should be boolean"
    assert isinstance(booking["bookingdates"], dict), "Bookingdates should be dict"
    

    assert "checkin" in booking["bookingdates"], "Should have checkin date"
    assert "checkout" in booking["bookingdates"], "Should have checkout date"




@pytest.mark.crud
def test_update_booking_full(auth_token, new_booking):
    """
    Test full update of booking (PUT)
    Expected: 200 status, all fields updated
    """
    booking_id = new_booking["id"]
    
    response = update_booking(
        booking_id=booking_id,
        token=auth_token,
        firstname="Updated",
        lastname="Name",
        totalprice=300,
        depositpaid=False,
        checkin="2025-12-15",
        checkout="2025-12-20",
        additionalneeds="Late checkout"
    )
    
    assert response.status_code == 200, \
        f"Expected status 200, got {response.status_code}"
    
    data = response.json()
    assert data["firstname"] == "Updated", "Firstname should be updated"
    assert data["lastname"] == "Name", "Lastname should be updated"
    assert data["totalprice"] == 300, "Price should be updated"
    assert data["depositpaid"] is False, "Deposit paid should be False"


@pytest.mark.crud
def test_partial_update_booking(auth_token, new_booking):
    """
    Test partial update of booking (PATCH)
    Expected: 200 status, only specified fields updated
    """
    booking_id = new_booking["id"]
    
    response = partial_update_booking(
        booking_id=booking_id,
        token=auth_token,
        firstname="PartiallyUpdated",
        totalprice=175
    )
    
    assert response.status_code == 200, \
        f"Expected status 200, got {response.status_code}"
    
    data = response.json()
    assert data["firstname"] == "PartiallyUpdated", "Firstname should be updated"
    assert data["totalprice"] == 175, "Price should be updated"
 
    assert data["lastname"] == "User", "Lastname should not change"


@pytest.mark.crud
def test_update_booking_requires_auth(new_booking):
    """
    Test that updating without auth token fails
    Expected: 403 Forbidden
    """
    booking_id = new_booking["id"]
    
    response = update_booking(
        booking_id=booking_id,
        token="invalid_token",
        firstname="Should",
        lastname="Fail",
        totalprice=100,
        depositpaid=True,
        checkin="2025-11-01",
        checkout="2025-11-05"
    )
    
    assert response.status_code == 403, \
        f"Expected status 403 for invalid auth, got {response.status_code}"



@pytest.mark.crud
def test_delete_booking_success(auth_token, new_booking):
    """
    Test deleting a booking
    Expected: 201 Created (yes, this API returns 201 for DELETE!)
    """
    booking_id = new_booking["id"]
    
    response = delete_booking(booking_id, auth_token)
    
    assert response.status_code == 201, \
        f"Expected status 201, got {response.status_code}"


@pytest.mark.crud
def test_delete_booking_requires_auth(new_booking):
    """
    Test that deleting without auth token fails
    Expected: 403 Forbidden
    """
    booking_id = new_booking["id"]
    
    response = delete_booking(booking_id, "invalid_token")
    
    assert response.status_code == 403, \
        f"Expected status 403 for invalid auth, got {response.status_code}"


@pytest.mark.crud
def test_deleted_booking_not_found(auth_token):
    """
    Test that deleted booking returns 404 when retrieved
    Expected: Create booking, delete it, then 404 on GET
    """

    create_response = create_booking(
        firstname="ToDelete",
        lastname="User",
        totalprice=100,
        depositpaid=True,
        checkin="2025-11-01",
        checkout="2025-11-02"
    )
    booking_id = create_response.json()["bookingid"]
    

    delete_response = delete_booking(booking_id, auth_token)
    assert delete_response.status_code == 201, "Deletion should succeed"
    

    get_response = get_booking_by_id(booking_id)
    assert get_response.status_code == 404, \
        f"Deleted booking should return 404, got {get_response.status_code}"