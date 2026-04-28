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
        client.post(reverse('todo-list'), {'title': 'Todo Item', 'status': 'todo'})
        resp = client.get(reverse('todo-list'), {'status': 'done'})
        assert resp.status_code == 200
        assert all(t['status'] == 'done' for t in resp.data['results'])
