"""
API Helper Functions for Restful-Booker API Testing
"""
import requests

BASE_URL = "https://restful-booker.herokuapp.com"


def health_check():
    """
    Check if API is responding
    Returns: Response object
    """
    url = f"{BASE_URL}/ping"
    response = requests.get(url)
    return response


def create_auth_token(username="admin", password="password123"):
    """
    Create authentication token
    Args:
        username: Admin username (default: admin)
        password: Admin password (default: password123)
    Returns: Token string or None if failed
    """
    url = f"{BASE_URL}/auth"
    headers = {"Content-Type": "application/json"}
    payload = {
        "username": username,
        "password": password
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("token")
    return None


def get_all_bookings():
    """
    Get list of all booking IDs
    Returns: Response object
    """
    url = f"{BASE_URL}/booking"
    response = requests.get(url)
    return response


def get_booking_by_id(booking_id):
    """
    Get specific booking details
    Args:
        booking_id: ID of the booking to retrieve
    Returns: Response object
    """
    url = f"{BASE_URL}/booking/{booking_id}"
    response = requests.get(url)
    return response


def create_booking(firstname, lastname, totalprice, depositpaid, 
                   checkin, checkout, additionalneeds=""):
    """
    Create a new booking
    Args:
        firstname: Guest first name
        lastname: Guest last name
        totalprice: Total price of booking
        depositpaid: Boolean - has deposit been paid
        checkin: Check-in date (YYYY-MM-DD)
        checkout: Check-out date (YYYY-MM-DD)
        additionalneeds: Additional needs (optional)
    Returns: Response object
    """
    url = f"{BASE_URL}/booking"
    headers = {"Content-Type": "application/json"}
    payload = {
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": totalprice,
        "depositpaid": depositpaid,
        "bookingdates": {
            "checkin": checkin,
            "checkout": checkout
        },
        "additionalneeds": additionalneeds
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response


def update_booking(booking_id, token, firstname, lastname, totalprice, 
                   depositpaid, checkin, checkout, additionalneeds=""):
    """
    Update an existing booking (full update)
    Args:
        booking_id: ID of booking to update
        token: Authentication token
        firstname: Guest first name
        lastname: Guest last name
        totalprice: Total price of booking
        depositpaid: Boolean - has deposit been paid
        checkin: Check-in date (YYYY-MM-DD)
        checkout: Check-out date (YYYY-MM-DD)
        additionalneeds: Additional needs (optional)
    Returns: Response object
    """
    url = f"{BASE_URL}/booking/{booking_id}"
    headers = {
        "Content-Type": "application/json",
        "Cookie": f"token={token}"
    }
    payload = {
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": totalprice,
        "depositpaid": depositpaid,
        "bookingdates": {
            "checkin": checkin,
            "checkout": checkout
        },
        "additionalneeds": additionalneeds
    }
    
    response = requests.put(url, json=payload, headers=headers)
    return response


def partial_update_booking(booking_id, token, **kwargs):
    """
    Partially update a booking
    Args:
        booking_id: ID of booking to update
        token: Authentication token
        **kwargs: Fields to update (firstname, lastname, totalprice, etc.)
    Returns: Response object
    """
    url = f"{BASE_URL}/booking/{booking_id}"
    headers = {
        "Content-Type": "application/json",
        "Cookie": f"token={token}"
    }
    
    response = requests.patch(url, json=kwargs, headers=headers)
    return response


def delete_booking(booking_id, token):
    """
    Delete a booking
    Args:
        booking_id: ID of booking to delete
        token: Authentication token
    Returns: Response object
    """
    url = f"{BASE_URL}/booking/{booking_id}"
    headers = {"Cookie": f"token={token}"}
    
    response = requests.delete(url, headers=headers)
    return response