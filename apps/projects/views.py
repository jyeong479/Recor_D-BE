from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Project, ProjectMember
from .serializers import ProjectSerializer, ProjectMemberSerializer
from .permissions import IsProjectMember, IsProjectOwnerOrAdmin


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(
            members__user=self.request.user
        ).prefetch_related('members__user').select_related('owner')


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsProjectMember]

    def get_queryset(self):
        return Project.objects.filter(members__user=self.request.user)


class ProjectMemberView(APIView):
    permission_classes = [IsProjectOwnerOrAdmin]

    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        self.check_object_permissions(request, project)
        members = project.members.select_related('user').all()
        return Response(ProjectMemberSerializer(members, many=True).data)

    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        self.check_object_permissions(request, project)
        serializer = ProjectMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(project=project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, project_id, user_id):
        project = get_object_or_404(Project, id=project_id)
        self.check_object_permissions(request, project)
        member = get_object_or_404(ProjectMember, project=project, user_id=user_id)
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
