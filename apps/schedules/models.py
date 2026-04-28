from django.db import models
from django.conf import settings
from common.models import TimeStampedModel


class Schedule(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='schedules'
    )
    project = models.ForeignKey(
        'projects.Project', on_delete=models.CASCADE,
        related_name='schedules', null=True, blank=True,
    )
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    is_all_day = models.BooleanField(default=False)
    location = models.CharField(max_length=300, blank=True)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='participating_schedules', blank=True
    )

    def __str__(self):
        return self.title
