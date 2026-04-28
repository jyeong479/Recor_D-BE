import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.accounts.models import User


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(email='user@test.com', username='user@test.com', password='pass')


@pytest.mark.django_db
class TestSchedule:
    def test_create_schedule(self, client, user):
        client.force_authenticate(user=user)
        resp = client.post(reverse('schedule-list'), {
            'title': 'Sprint Meeting',
            'start_datetime': '2026-05-01T10:00:00+09:00',
            'end_datetime': '2026-05-01T11:00:00+09:00',
        })
        assert resp.status_code == 201

    def test_invalid_datetime_range(self, client, user):
        client.force_authenticate(user=user)
        resp = client.post(reverse('schedule-list'), {
            'title': 'Bad Schedule',
            'start_datetime': '2026-05-01T11:00:00+09:00',
            'end_datetime': '2026-05-01T10:00:00+09:00',
        })
        assert resp.status_code == 400
