from django.contrib import admin
from .models import Portfolio, StarEntry


class StarEntryInline(admin.StackedInline):
    model = StarEntry
    extra = 0


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'project', 'is_public', 'created_at')
    list_filter = ('is_public',)
    inlines = [StarEntryInline]
