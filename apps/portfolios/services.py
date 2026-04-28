from django.utils import timezone
from core.ai.services import generate_star_summary
from .models import StarEntry


def summarize_star_entry(entry: StarEntry) -> StarEntry:
    summary = generate_star_summary(
        situation=entry.situation,
        task=entry.task,
        action=entry.action,
        result=entry.result,
    )
    entry.ai_summary = summary
    entry.is_summarized = True
    entry.summarized_at = timezone.now()
    entry.save(update_fields=['ai_summary', 'is_summarized', 'summarized_at'])
    return entry
