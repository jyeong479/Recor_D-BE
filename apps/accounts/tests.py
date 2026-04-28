import pytest
from django.urls import reverse
from unittest.mock import patch
from rest_framework.test import APIClient
from .models import User


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email='test@example.com',
        username='test@example.com',
        password='testpass123',
        name='Test User',
    )


@pytest.mark.django_db
class TestSocialLogin:
    def test_google_login_creates_new_user(self, client):
        mock_data = {'sub': '12345', 'email': 'new@example.com', 'name': 'New User', 'picture': ''}
        with patch('apps.accounts.services.requests.get') as mock_get:
            mock_get.return_value.json.return_value = mock_data
            mock_get.return_value.raise_for_status = lambda: None
            resp = client.post(reverse('social-login'), {
                'provider': 'google',
                'access_token': 'valid-token',
            })
        assert resp.status_code == 200
        assert resp.data['is_new_user'] is True
        assert 'access' in resp.data


@pytest.mark.django_db
class TestProfile:
    def test_get_profile(self, client, user):
        client.force_authenticate(user=user)
        resp = client.get(reverse('profile'))
        assert resp.status_code == 200
        assert resp.data['email'] == user.email
