from django.contrib import admin
from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'project', 'status', 'priority', 'due_date')
    list_filter = ('status', 'priority')
