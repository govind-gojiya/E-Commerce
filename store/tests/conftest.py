from django.contrib.auth.models import User
from rest_framework.test import APIClient
import pytest


# Global fixture defined in this conftest.py file
# Fixture use to avoid repeated code in test
@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def autheticate(api_client):
    def do_autheticate(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_autheticate
