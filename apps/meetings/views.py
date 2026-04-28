from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.projects.models import ProjectMember
from .models import Meeting, MeetingNote
from .serializers import MeetingSerializer, MeetingNoteSerializer
from .services import summarize_note


class MeetingListCreateView(generics.ListCreateAPIView):
    serializer_class = MeetingSerializer

    def get_queryset(self):
        user_projects = ProjectMember.objects.filter(user=self.request.user).values_list('project_id', flat=True)
        return Meeting.objects.filter(project_id__in=user_projects).select_related('project', 'note')


class MeetingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MeetingSerializer

    def get_queryset(self):
        user_projects = ProjectMember.objects.filter(user=self.request.user).values_list('project_id', flat=True)
        return Meeting.objects.filter(project_id__in=user_projects)


class MeetingNoteView(APIView):
    def get_meeting(self, meeting_id, user):
        user_projects = ProjectMember.objects.filter(user=user).values_list('project_id', flat=True)
        return get_object_or_404(Meeting, id=meeting_id, project_id__in=user_projects)

    def get(self, request, meeting_id):
        meeting = self.get_meeting(meeting_id, request.user)
        note = get_object_or_404(MeetingNote, meeting=meeting)
        return Response(MeetingNoteSerializer(note).data)

    def put(self, request, meeting_id):
        meeting = self.get_meeting(meeting_id, request.user)
        note, _ = MeetingNote.objects.get_or_create(meeting=meeting)
        serializer = MeetingNoteSerializer(note, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class MeetingNoteSummarizeView(APIView):
    def post(self, request, meeting_id):
        user_projects = ProjectMember.objects.filter(user=request.user).values_list('project_id', flat=True)
        meeting = get_object_or_404(Meeting, id=meeting_id, project_id__in=user_projects)
        note = get_object_or_404(MeetingNote, meeting=meeting)

        if not note.content:
            return Response({'error': '회의록 내용이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        note = summarize_note(note)
        return Response(MeetingNoteSerializer(note).data)
