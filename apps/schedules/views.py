from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Schedule
from .serializers import ScheduleSerializer


class ScheduleListCreateView(generics.ListCreateAPIView):
    serializer_class = ScheduleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project', 'is_all_day']

    def get_queryset(self):
        qs = Schedule.objects.filter(user=self.request.user)
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        if start:
            qs = qs.filter(start_datetime__gte=start)
        if end:
            qs = qs.filter(end_datetime__lte=end)
        return qs.select_related('project').prefetch_related('participants')


class ScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        return Schedule.objects.filter(user=self.request.user)
