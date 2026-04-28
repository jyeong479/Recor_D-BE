from django.db import models
from django.conf import settings
from common.models import TimeStampedModel


class Portfolio(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='portfolios'
    )
    project = models.ForeignKey(
        'projects.Project', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='portfolios',
    )
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    tech_stack = models.JSONField(default=list)
    github_url = models.URLField(blank=True)
    deploy_url = models.URLField(blank=True)
    thumbnail_url = models.URLField(blank=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class StarEntry(TimeStampedModel):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='star_entries')
    situation = models.TextField(verbose_name='상황 (Situation)')
    task = models.TextField(verbose_name='목표/과제 (Task)')
    action = models.TextField(verbose_name='행동 (Action)')
    result = models.TextField(verbose_name='결과 (Result)')
    ai_summary = models.TextField(blank=True)
    is_summarized = models.BooleanField(default=False)
    summarized_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"STAR: {self.portfolio.title}"
