"""task_manager.statuses.admin module."""
from django.contrib import admin
from task_manager.statuses.forms import StatusCreateForm, StatusUpdateForm
from task_manager.statuses.models import Status


class StatusAdmin(admin.ModelAdmin):
    """View for Status model in admin site."""

    add_form = StatusCreateForm
    form = StatusUpdateForm
    model = Status
    list_display = ('id', 'name', 'created_at')
    list_filter = ('name', 'created_at')
    search_fields = ('name',)


admin.site.register(Status, StatusAdmin)
