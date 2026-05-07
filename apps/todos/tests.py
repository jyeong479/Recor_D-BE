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
class TestTodo:
    def test_create_todo(self, client, user):
        client.force_authenticate(user=user)
        resp = client.post(reverse('todo-list'), {'title': 'Test Todo', 'priority': 'high'})
        assert resp.status_code == 201
        assert resp.data['title'] == 'Test Todo'

    def test_filter_by_status(self, client, user):
        client.force_authenticate(user=user)
        client.post(reverse('todo-list'), {'title': 'Done Todo', 'status': 'done'})
        client.post(reverse('todo-list'), {'title': 'In Progress Todo', 'status': 'in_progress'})
        resp = client.get(reverse('todo-list'), {'status': 'done'})
        assert resp.status_code == 200
        assert all(t['status'] == 'done' for t in resp.data['results'])

    def test_default_status_is_in_progress(self, client, user):
        client.force_authenticate(user=user)
        resp = client.post(reverse('todo-list'), {'title': 'Default Status Todo'})
        assert resp.status_code == 201
        assert resp.data['status'] == 'in_progress'

    def test_filter_by_due_date_range(self, client, user):
        client.force_authenticate(user=user)
        client.post(reverse('todo-list'), {'title': 'April Todo', 'due_date': '2026-04-15'})
        client.post(reverse('todo-list'), {'title': 'May Todo', 'due_date': '2026-05-01'})
        resp = client.get(reverse('todo-list'), {
            'due_date_after': '2026-04-01',
            'due_date_before': '2026-04-30',
        })
        assert resp.status_code == 200
        assert [todo['title'] for todo in resp.data['results']] == ['April Todo']
