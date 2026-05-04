from django.utils import timezone
from core.ai.services import summarize_meeting_note
from .models import Meeting


def summarize_meeting(meeting: Meeting) -> Meeting:
    content = meeting.transcript or meeting.summary
    summary = summarize_meeting_note(content)
    meeting.ai_summary = summary
    meeting.is_summarized = True
    meeting.summarized_at = timezone.now()
    meeting.save(update_fields=['ai_summary', 'is_summarized', 'summarized_at'])
    return meeting
