from django.db import models
from django.conf import settings
from common.models import TimeStampedModel


class Meeting(TimeStampedModel):
    project = models.ForeignKey(
        'projects.Project', on_delete=models.CASCADE, related_name='meetings'
    )
    title = models.CharField(max_length=300)
    held_at = models.DateTimeField()
    location = models.CharField(max_length=300, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='created_meetings',
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='attended_meetings', blank=True
    )

    def __str__(self):
        return f"{self.project.name} - {self.title}"


class MeetingNote(TimeStampedModel):
    meeting = models.OneToOneField(Meeting, on_delete=models.CASCADE, related_name='note')
    content = models.TextField()
    ai_summary = models.TextField(blank=True)
    is_summarized = models.BooleanField(default=False)
    summarized_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Note: {self.meeting.title}"
