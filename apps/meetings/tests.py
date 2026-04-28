import pytest
from django.urls import reverse
from unittest.mock import patch
from rest_framework.test import APIClient
from apps.accounts.models import User
from apps.projects.models import Project, ProjectMember
from .models import Meeting, MeetingNote


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(email='user@test.com', username='user@test.com', password='pass')


@pytest.fixture
def project(db, user):
    project = Project.objects.create(name='Test Project', owner=user)
    ProjectMember.objects.create(project=project, user=user, role='owner')
    return project


@pytest.fixture
def meeting(db, project, user):
    return Meeting.objects.create(
        project=project, title='Sprint Retro',
        held_at='2026-05-01T10:00:00+09:00', created_by=user,
    )


@pytest.mark.django_db
class TestMeetingNoteSummarize:
    def test_summarize_note(self, client, user, meeting):
        client.force_authenticate(user=user)
        MeetingNote.objects.create(meeting=meeting, content='회의 내용입니다.')

        with patch('apps.meetings.services.summarize_meeting_note', return_value='AI 요약 결과'):
            resp = client.post(reverse('meeting-note-summarize', kwargs={'meeting_id': meeting.id}))

        assert resp.status_code == 200
        assert resp.data['ai_summary'] == 'AI 요약 결과'
        assert resp.data['is_summarized'] is True
