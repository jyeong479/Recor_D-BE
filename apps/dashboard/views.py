from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.projects.models import Project
from apps.schedules.models import Schedule
from apps.todos.models import Todo


class DashboardView(APIView):
    def get(self, request):
        user = request.user
        today = timezone.localdate()

        active_projects = Project.objects.filter(
            owner=user, status='진행중'
        ).prefetch_related('todos')

        active_projects_data = [
            {
                'id': p.id,
                'name': p.name,
                'color': p.color,
                'todo_count': p.todos.count(),
                'completed_todo_count': p.todos.filter(status='done').count(),
            }
            for p in active_projects
        ]

        today_start = timezone.make_aware(
            timezone.datetime.combine(today, timezone.datetime.min.time())
        )
        today_end = timezone.make_aware(
            timezone.datetime.combine(today, timezone.datetime.max.time())
        )
        today_schedules = Schedule.objects.filter(
            user=user,
            start_datetime__gte=today_start,
            start_datetime__lte=today_end,
        ).order_by('start_datetime')

        today_schedules_data = [
            {
                'id': s.id,
                'title': s.title,
                'start_datetime': s.start_datetime,
                'type': s.type,
                'location': s.location,
            }
            for s in today_schedules
        ]

        today_todos = Todo.objects.filter(
            user=user,
            due_date__lte=today,
        ).exclude(status='done').order_by('due_date')

        today_todos_data = [
            {
                'id': t.id,
                'title': t.title,
                'due_date': t.due_date,
                'priority': t.priority,
                'status': t.status,
                'project_id': t.project_id,
            }
            for t in today_todos
        ]

        return Response({
            'active_projects': active_projects_data,
            'today_schedules': today_schedules_data,
            'today_todos': today_todos_data,
        })
