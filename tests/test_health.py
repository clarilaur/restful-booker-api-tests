"""
Health Check Tests
Verify API is running and responsive
"""
import pytest
from utils.api_helpers import health_check


@pytest.mark.smoke
def test_api_is_running():
    """
    Test that API responds to health check ping
    Expected: 201 Created status
    """
    response = health_check()
    
    assert response.status_code == 201, \
        f"Expected status 201, got {response.status_code}"


@pytest.mark.smoke
def test_health_check_response_time():
    """
    Test that health check responds quickly
    Expected: Response time under 2 seconds
    """
    response = health_check()
    
    response_time = response.elapsed.total_seconds()
    assert response_time < 2.0, \
        f"Response time too slow: {response_time}s (expected < 2s)"


def test_health_check_content():
    """
    Test that health check returns expected content
    Expected: "Created" text in response
    """
    response = health_check()
    
    assert "Created" in response.text, \
        f"Expected 'Created' in response, got: {response.text}"