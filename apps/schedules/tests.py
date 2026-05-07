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
            'type': 'meeting',
            'start_datetime': '2026-05-01T10:00:00+09:00',
            'end_datetime': '2026-05-01T11:00:00+09:00',
        })
        assert resp.status_code == 201
        assert resp.data['type'] == 'meeting'
        assert resp.data['color'] == 'primary'

    def test_invalid_datetime_range(self, client, user):
        client.force_authenticate(user=user)
        resp = client.post(reverse('schedule-list'), {
            'title': 'Bad Schedule',
            'start_datetime': '2026-05-01T11:00:00+09:00',
            'end_datetime': '2026-05-01T10:00:00+09:00',
        })
        assert resp.status_code == 400

    def test_order_schedules_by_start_datetime(self, client, user):
        client.force_authenticate(user=user)
        client.post(reverse('schedule-list'), {
            'title': 'Later',
            'start_datetime': '2026-05-01T13:00:00+09:00',
            'end_datetime': '2026-05-01T14:00:00+09:00',
        })
        client.post(reverse('schedule-list'), {
            'title': 'Earlier',
            'start_datetime': '2026-05-01T10:00:00+09:00',
            'end_datetime': '2026-05-01T11:00:00+09:00',
        })
        resp = client.get(reverse('schedule-list'), {'ordering': 'start_datetime'})
        assert resp.status_code == 200
        assert [schedule['title'] for schedule in resp.data['results']] == ['Earlier', 'Later']
