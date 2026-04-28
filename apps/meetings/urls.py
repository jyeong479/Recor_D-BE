from django.urls import path
from .views import MeetingListCreateView, MeetingDetailView, MeetingNoteView, MeetingNoteSummarizeView

urlpatterns = [
    path('', MeetingListCreateView.as_view(), name='meeting-list'),
    path('<int:pk>/', MeetingDetailView.as_view(), name='meeting-detail'),
    path('<int:meeting_id>/note/', MeetingNoteView.as_view(), name='meeting-note'),
    path('<int:meeting_id>/note/summarize/', MeetingNoteSummarizeView.as_view(), name='meeting-note-summarize'),
]
