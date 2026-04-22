import pytest
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    # Sử dụng APIClient của DRF cho các test API toàn cục
    return APIClient()
