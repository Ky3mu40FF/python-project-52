"""task_manager.statuses.forms module."""
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from task_manager.statuses.models import Status


class StatusCreateForm(ModelForm):
    """Task's Status creation form."""

    class Meta(ModelForm):
        model = Status
        fields = ('name',)
        labels = {
            'name': _('Name'),
        }


class StatusUpdateForm(ModelForm):
    """Task's Status updating form."""

    class Meta(ModelForm):
        model = Status
        fields = ('name',)
        labels = {
            'name': _('Name'),
        }
