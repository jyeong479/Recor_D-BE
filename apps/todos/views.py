from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Todo
from .serializers import TodoSerializer


class TodoListCreateView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'priority', 'project', 'due_date']
    ordering_fields = ['due_date', 'priority', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user).select_related('project', 'assigned_to')


class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)
