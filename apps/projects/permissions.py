from rest_framework.permissions import BasePermission
from .models import ProjectMember


class IsProjectMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        project = getattr(obj, 'project', obj)
        return ProjectMember.objects.filter(project=project, user=request.user).exists()


class IsProjectOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        project = getattr(obj, 'project', obj)
        return ProjectMember.objects.filter(
            project=project, user=request.user, role__in=['owner', 'admin']
        ).exists()
