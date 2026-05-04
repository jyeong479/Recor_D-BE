from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Meeting
from .serializers import MeetingSerializer
from .services import summarize_meeting


class MeetingListCreateView(generics.ListCreateAPIView):
    serializer_class = MeetingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project']

    def get_queryset(self):
        return Meeting.objects.filter(created_by=self.request.user).select_related('project')


class MeetingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MeetingSerializer

    def get_queryset(self):
        return Meeting.objects.filter(created_by=self.request.user)


class MeetingSummarizeView(APIView):
    def post(self, request, pk):
        meeting = Meeting.objects.filter(created_by=request.user).filter(pk=pk).first()
        if not meeting:
            return Response({'error': '회의록을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        if not meeting.transcript and not meeting.summary:
            return Response({'error': '요약할 내용이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        meeting = summarize_meeting(meeting)
        return Response(MeetingSerializer(meeting).data)
