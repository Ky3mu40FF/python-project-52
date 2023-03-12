"""task_manager.labels.forms module."""
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from task_manager.labels.models import Label


class LabelCreateForm(ModelForm):
    """Label creation form."""

    class Meta:
        model = Label
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})


class LabelUpdateForm(ModelForm):
    """Label updating form."""

    class Meta:
        model = Label
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
