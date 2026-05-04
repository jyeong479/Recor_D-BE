from django.urls import path
from .views import MeetingListCreateView, MeetingDetailView, MeetingSummarizeView

urlpatterns = [
    path('', MeetingListCreateView.as_view(), name='meeting-list'),
    path('<int:pk>/', MeetingDetailView.as_view(), name='meeting-detail'),
    path('<int:pk>/summarize/', MeetingSummarizeView.as_view(), name='meeting-summarize'),
]
