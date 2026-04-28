from django.contrib import admin
from .models import Meeting, MeetingNote


class MeetingNoteInline(admin.StackedInline):
    model = MeetingNote
    extra = 0


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'held_at', 'created_by')
    inlines = [MeetingNoteInline]
