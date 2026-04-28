from django.utils import timezone
from core.ai.services import summarize_meeting_note
from .models import MeetingNote


def summarize_note(note: MeetingNote) -> MeetingNote:
    summary = summarize_meeting_note(note.content)
    note.ai_summary = summary
    note.is_summarized = True
    note.summarized_at = timezone.now()
    note.save(update_fields=['ai_summary', 'is_summarized', 'summarized_at'])
    return note
