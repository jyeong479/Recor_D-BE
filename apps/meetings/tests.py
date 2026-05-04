import pytest
from django.urls import reverse
from unittest.mock import patch
from rest_framework.test import APIClient
from apps.accounts.models import User
from .models import Meeting


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(email='user@test.com', username='user@test.com', password='pass')


@pytest.fixture
def meeting(db, user):
    return Meeting.objects.create(
        title='Sprint Retro',
        date='2026-05-01',
        created_by=user,
    )


@pytest.mark.django_db
class TestMeetingSummarize:
    def test_summarize_meeting(self, client, user, meeting):
        meeting.transcript = '회의 내용입니다.'
        meeting.save()
        client.force_authenticate(user=user)

        with patch('apps.meetings.services.summarize_meeting_note', return_value='AI 요약 결과'):
            resp = client.post(reverse('meeting-summarize', kwargs={'pk': meeting.id}))

        assert resp.status_code == 200
        assert resp.data['ai_summary'] == 'AI 요약 결과'
        assert resp.data['is_summarized'] is True

    def test_summarize_without_content(self, client, user, meeting):
        client.force_authenticate(user=user)
        resp = client.post(reverse('meeting-summarize', kwargs={'pk': meeting.id}))
        assert resp.status_code == 400

    def test_create_meeting(self, client, user):
        client.force_authenticate(user=user)
        resp = client.post(reverse('meeting-list'), {
            'title': '기획 회의',
            'date': '2026-05-01',
            'participants': '김철수, 이영희',
            'duration': '45분',
        })
        assert resp.status_code == 201
        assert resp.data['title'] == '기획 회의'
