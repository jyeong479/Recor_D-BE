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
        MeetingNote.objects.create(meeting=meeting, content='meeting note content')

        with patch('apps.meetings.services.summarize_meeting_note', return_value='AI summary result'):
            resp = client.post(reverse('meeting-note-summarize', kwargs={'meeting_id': meeting.id}))

        assert resp.status_code == 200
        assert resp.data['ai_summary'] == 'AI summary result'
        assert resp.data['is_summarized'] is True


@pytest.mark.django_db
class TestMeetingPermissions:
    def test_create_meeting_rejects_non_member_project(self, client, user):
        other = User.objects.create_user(
            email='other@test.com',
            username='other@test.com',
            password='pass',
        )
        other_project = Project.objects.create(name='Other Project', owner=other)
        ProjectMember.objects.create(project=other_project, user=other, role='owner')

        client.force_authenticate(user=user)
        resp = client.post(reverse('meeting-list'), {
            'project': other_project.id,
            'title': 'Unauthorized Meeting',
            'held_at': '2026-05-01T10:00:00+09:00',
        })

        assert resp.status_code == 400
        assert Meeting.objects.filter(title='Unauthorized Meeting').count() == 0

    def test_create_meeting_rejects_non_project_participant(self, client, user, project):
        outsider = User.objects.create_user(
            email='outsider@test.com',
            username='outsider@test.com',
            password='pass',
        )

        client.force_authenticate(user=user)
        resp = client.post(reverse('meeting-list'), {
            'project': project.id,
            'title': 'Team Meeting',
            'held_at': '2026-05-01T10:00:00+09:00',
            'participants': [outsider.id],
        }, format='json')

        assert resp.status_code == 400
        assert Meeting.objects.filter(title='Team Meeting').count() == 0

    def test_update_project_rejects_existing_non_project_participant(
        self, client, user, project, meeting
    ):
        teammate = User.objects.create_user(
            email='teammate@test.com',
            username='teammate@test.com',
            password='pass',
        )
        ProjectMember.objects.create(project=project, user=teammate, role='member')
        meeting.participants.add(teammate)

        other_project = Project.objects.create(name='Other Project', owner=user)
        ProjectMember.objects.create(project=other_project, user=user, role='owner')

        client.force_authenticate(user=user)
        resp = client.patch(reverse('meeting-detail', kwargs={'pk': meeting.id}), {
            'project': other_project.id,
        }, format='json')

        assert resp.status_code == 400
