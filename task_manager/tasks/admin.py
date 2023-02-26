from django.contrib import admin
from task_manager.tasks.forms import (
    TaskCreateForm,
    TaskUpdateForm,
)
from task_manager.tasks.models import Task


class TaskAdmin(admin.ModelAdmin):
    """View for Task model in admin site."""

    add_form = TaskCreateForm
    form = TaskUpdateForm
    model = Task
    list_display = ('id', 'name', 'status', 'author', 'executor', 'created_at')
    list_filter = ('name', 'status', 'author', 'executor', 'created_at')
    search_fields = ('name', 'description', 'status', 'author', 'executor')


admin.site.register(Task)
