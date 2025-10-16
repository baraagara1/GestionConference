from django.contrib import admin
from .models import Session
# Register your models here.
admin.site.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'session_day', 'start_time', 'end_time', 'room', 'conference')
    ordering = ('session_day',)
    search_fields = ('title', 'topic', 'room', 'conference__name')
    list_filter = ('session_day', 'conference__start_date', 'conference__end_date')
    date_hierarchy = 'session_day'
    fieldsets = (
        ('Informations générales', {
            'fields': ('session_id','title', 'topic', 'room', 'session_day', 'start_time', 'end_time', 'conference')
        }),
    )
    readonly_fields = ('session_id',)
    ordering = ('-session_day',)
    
