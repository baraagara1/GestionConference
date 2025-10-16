from django.contrib import admin
from .models import User
# Register your models here.
admin.site.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_active", "is_staff", "date_joined")
    search_fields = ("username", "email", "first_name", "last_name")
    list_filter = ("is_active", "is_staff", "date_joined")
    ordering = ("username",)
