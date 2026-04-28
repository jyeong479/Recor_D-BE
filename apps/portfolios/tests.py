import pytest
from django.urls import reverse
from unittest.mock import patch
from rest_framework.test import APIClient
from apps.accounts.models import User
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
        situation='팀 내 코드 리뷰 문화가 없었음',
        task='코드 품질 향상을 위한 리뷰 프로세스 도입',
        action='PR 템플릿 작성 및 리뷰 가이드라인 수립',
        result='버그 발생률 30% 감소',
    )


@pytest.mark.django_db
class TestStarSummarize:
    def test_summarize_star_entry(self, client, user, portfolio, star_entry):
        client.force_authenticate(user=user)

        with patch('apps.portfolios.services.generate_star_summary', return_value='STAR 요약 결과'):
            resp = client.post(reverse('star-summarize', kwargs={
                'portfolio_id': portfolio.id,
                'pk': star_entry.id,
            }))

        assert resp.status_code == 200
        assert resp.data['ai_summary'] == 'STAR 요약 결과'
        assert resp.data['is_summarized'] is True
