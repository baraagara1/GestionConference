from django.contrib import admin
from .models import OrganizingCommittee
# Register your models here.
admin.site.register(OrganizingCommittee)
class OrganizingCommitteeAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "conference")
    search_fields = ("name", "role", "conference__name")
    list_filter = ("role", "conference")
    ordering = ("name",)
    
    