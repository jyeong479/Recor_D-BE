from django.db import models
from django.conf import settings
from common.models import TimeStampedModel


class Meeting(TimeStampedModel):
    project = models.ForeignKey(
        'projects.Project', on_delete=models.SET_NULL,
        related_name='meetings', null=True, blank=True,
    )
    title = models.CharField(max_length=300)
    date = models.DateField()
    duration = models.CharField(max_length=50, blank=True)
    participants = models.CharField(max_length=500, blank=True)
    summary = models.TextField(blank=True)
    tags = models.JSONField(default=list)
    transcript = models.TextField(blank=True)
    ai_summary = models.TextField(blank=True)
    key_points = models.JSONField(default=list)
    action_items = models.JSONField(default=list)
    is_summarized = models.BooleanField(default=False)
    summarized_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='created_meetings',
    )

    def __str__(self):
        return self.title
