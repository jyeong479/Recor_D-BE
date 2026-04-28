from django.db import models
from django.conf import settings
from common.models import TimeStampedModel


class Project(TimeStampedModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_projects'
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ProjectMember(TimeStampedModel):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('member', 'Member'),
        ('viewer', 'Viewer'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_memberships'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')

    class Meta:
        unique_together = ('project', 'user')

    def __str__(self):
        return f"{self.project.name} - {self.user.email} ({self.role})"
