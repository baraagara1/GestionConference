from django.contrib import admin
from .models import Submissions

@admin.action(description="Marquer comme payées")
def mark_as_payed(modeladmin, request, queryset):
    queryset.update(payed=True)

@admin.action(description="Accepter les soumissions sélectionnées")
def accept_submissions(modeladmin, request, queryset):
    queryset.update(status="accepted")

@admin.register(Submissions)
class SubmissionAdmin(admin.ModelAdmin):
    # a, b, c
    list_display = ("title", "status", "user", "conference", "submission_date", "payed", "short_abstract")
    
    def short_abstract(self, obj):
        if len(obj.abstract) > 50:
            return obj.abstract[:50] + "..."
        return obj.abstract
    short_abstract.short_description = "Abstract (50)"
    
    # d, e
    list_filter = ("status", "payed", "conference", "submission_date")
    search_fields = ("title", "keywords", "user__username")
    
    # f
    list_editable = ("status", "payed")
    
    # g, h
    fieldsets = (
        ("Infos générales", {
            "fields": ("submission_id", "title", "abstract", "keywords")
        }),
        ("Fichier et conférence", {
            "fields": ("paper", "conference")
        }),
        ("Suivi", {
            "fields": ("status", "payed", "submission_date", "user")
        }),
    )
    readonly_fields = ("submission_id", "submission_date")
    
    # j, k
    actions = [mark_as_payed, accept_submissions]
    ordering = ("-submission_date",)