"""task_manager.labels.forms module."""
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from task_manager.labels.models import Label


class LabelCreateForm(ModelForm):
    """Label creation form."""

    class Meta:
        model = Label
        fields = ('name',)
        labels = {
            'name': _('Name'),
        }


class LabelUpdateForm(ModelForm):
    """Label updating form."""

    class Meta:
        model = Label
        fields = ('name',)
        labels = {
            'name': _('Name'),
        }
