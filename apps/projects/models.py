from django.db import models
from django.conf import settings
from common.models import TimeStampedModel


class Project(TimeStampedModel):
    STATUS_CHOICES = [
        ('진행중', '진행중'),
        ('완료', '완료'),
        ('중단', '중단'),
    ]
    COLOR_CHOICES = [
        ('primary', 'primary'),
        ('accent', 'accent'),
        ('secondary', 'secondary'),
        ('success', 'success'),
        ('warning', 'warning'),
        ('destructive', 'destructive'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_projects'
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='진행중')
    tags = models.JSONField(default=list)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='primary')

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
