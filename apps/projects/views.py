from rest_framework import generics

from .models import Project
from .serializers import ProjectSerializer


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(
            owner=self.request.user
        ).prefetch_related('meetings', 'todos', 'schedules').order_by('-created_at')


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(
            owner=self.request.user
        ).prefetch_related('meetings', 'todos', 'schedules')
