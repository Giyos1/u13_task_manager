from django.contrib import admin

from tasks.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass