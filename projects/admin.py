from django.contrib import admin
from .models import Project

# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "creator", "status", "duration", "created_at")
    list_filter = ("status",)
    search_fields = ("title", "creator__username")
    ordering = ("-created_at",)