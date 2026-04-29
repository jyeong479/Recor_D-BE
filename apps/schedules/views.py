from django.utils.dateparse import parse_datetime, parse_date
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from .models import Schedule
from .serializers import ScheduleSerializer


def _parse_datetime_param(value, field_name):
    if parse_datetime(value) is None and parse_date(value) is None:
        raise ValidationError({field_name: '올바른 날짜 형식이 아닙니다. (예: 2026-01-01 또는 2026-01-01T00:00:00)'})
    return value


class ScheduleListCreateView(generics.ListCreateAPIView):
    serializer_class = ScheduleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project', 'is_all_day']

    def get_queryset(self):
        qs = Schedule.objects.filter(user=self.request.user)
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        if start:
            qs = qs.filter(start_datetime__gte=_parse_datetime_param(start, 'start'))
        if end:
            qs = qs.filter(end_datetime__lte=_parse_datetime_param(end, 'end'))
        return qs.select_related('project').prefetch_related('participants')


class ScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        return Schedule.objects.filter(user=self.request.user)
