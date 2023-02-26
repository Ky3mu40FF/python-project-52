"""task_manager.statuses.forms module."""
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from task_manager.statuses.models import Status


class StatusCreateForm(ModelForm):
    """Task's Status creation form."""

    class Meta:
        model = Status
        fields = ('name',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})


class StatusUpdateForm(ModelForm):
    """Task's Status updating form."""

    class Meta:
        model = Status
        fields = ('name',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
