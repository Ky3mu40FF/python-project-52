from django.contrib import admin
from task_manager.labels.forms import (
    LabelCreateForm,
    LabelUpdateForm,
)
from task_manager.labels.models import Label


class LabelAdmin(admin.ModelAdmin):
    """View for Label model in admin site."""

    add_form = LabelCreateForm
    form = LabelUpdateForm
    model = Label
    list_display = ('id', 'name', 'created_at')
    list_filter = ('name', 'created_at')
    search_fields = ('name',)


admin.site.register(Label, LabelAdmin)
