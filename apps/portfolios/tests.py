import pytest
from django.urls import reverse
from unittest.mock import patch
from rest_framework.test import APIClient
from apps.accounts.models import User
from apps.projects.models import Project, ProjectMember
from .models import Portfolio, StarEntry


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(email='user@test.com', username='user@test.com', password='pass')


@pytest.fixture
def portfolio(db, user):
    return Portfolio.objects.create(user=user, title='My Portfolio')


@pytest.fixture
def star_entry(db, portfolio):
    return StarEntry.objects.create(
        portfolio=portfolio,
        situation='There was no code review culture.',
        task='Introduce a review process to improve code quality.',
        action='Created a PR template and review guidelines.',
        result='Reduced bug reports by 30%.',
    )


@pytest.mark.django_db
class TestStarSummarize:
    def test_summarize_star_entry(self, client, user, portfolio, star_entry):
        client.force_authenticate(user=user)

        with patch('apps.portfolios.services.generate_star_summary', return_value='STAR summary result'):
            resp = client.post(reverse('star-summarize', kwargs={
                'portfolio_id': portfolio.id,
                'pk': star_entry.id,
            }))

        assert resp.status_code == 200
        assert resp.data['ai_summary'] == 'STAR summary result'
        assert resp.data['is_summarized'] is True


@pytest.mark.django_db
class TestPortfolioPermissions:
    def test_create_portfolio_rejects_non_member_project(self, client, user):
        other = User.objects.create_user(
            email='other@test.com',
            username='other@test.com',
            password='pass',
        )
        other_project = Project.objects.create(name='Other Project', owner=other)
        ProjectMember.objects.create(project=other_project, user=other, role='owner')

        client.force_authenticate(user=user)
        resp = client.post(reverse('portfolio-list'), {
            'project': other_project.id,
            'title': 'Unauthorized Portfolio',
        })

        assert resp.status_code == 400
        assert Portfolio.objects.filter(title='Unauthorized Portfolio').count() == 0

    def test_star_detail_requires_matching_portfolio_id(self, client, user, star_entry):
        other_portfolio = Portfolio.objects.create(user=user, title='Other Portfolio')

        client.force_authenticate(user=user)
        resp = client.get(reverse('star-detail', kwargs={
            'portfolio_id': other_portfolio.id,
            'pk': star_entry.id,
        }))

        assert resp.status_code == 404
