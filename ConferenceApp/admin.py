from django.contrib import admin
from .models import Conference
from SubmissionApp.models import Submissions
from django.utils.html import format_html
from django.utils import timezone

admin.site.site_header = "Conference Management Admin"
admin.site.site_title = "Conference Management Admin Portal"
admin.site.index_title = "Welcome to Conference Management Portal"

class SubmissionStackedInline(admin.StackedInline):
    model = Submissions
    extra = 0
    fields = ("submission_id", "title", "abstract", "status", "payed", "user", "paper", "submission_date")
    readonly_fields = ("submission_id", "submission_date")

class SubmissionInline(admin.TabularInline):
    model = Submissions
    extra = 0
    fields = ("submission_id", "title", "status", "payed", "user", "submission_date")
    readonly_fields = ("submission_id", "submission_date")

@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'theme', 'location', 'start_date', 'end_date', 'duration', 'submission_count')
    ordering = ('-start_date',)
    list_per_page = 10
    search_fields = ('name', 'location', 'description')
    list_filter = ('theme', 'location', 'start_date')
    date_hierarchy = 'start_date'

    fieldsets = (
        ('Informations générales', {
            'fields': ('conference_id', 'name', 'theme', 'description')
        }),
        ('Logistique', {
            'fields': ('location', 'start_date', 'end_date'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('conference_id',)

    def duration(self, obj):
        if obj.start_date and obj.end_date:
            return (obj.end_date - obj.start_date).days
        return "—"
    duration.short_description = 'Durée (jours)'
    duration.admin_order_field = 'end_date'

    def submission_count(self, obj):
        return obj.submissions.count()
    submission_count.short_description = "Nb de soumissions"

    inlines = [SubmissionInline]  # ou [SubmissionStackedInline]
