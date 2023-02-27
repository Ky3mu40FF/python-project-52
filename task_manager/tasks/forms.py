"""task_manager.statuses.forms module."""
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskCreateForm(ModelForm):
    """Task creation form."""

    class Meta:
        model = Task
        fields = (
            'name',
            'description',
            'status',
            'author',
            'executor',
            # 'tags',
        )
        labels = {
            'name': _('Name'),
            'description': _('Description'),
            'status': _('Status'),
            'author': _('Author'),
            'executor': _('Executor'),
            'tags': _('Tags'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['status'].widget.attrs.update({'class': 'form-control'})
        self.fields['executor'].widget.attrs.update({'class': 'form-control'})
        # self.fields['tags'].widget.attrs.update({'class': 'form-control'})


class TaskUpdateForm(ModelForm):
    """Task updating form."""

    class Meta:
        model = Task
        fields = (
            'name',
            'description',
            'status',
            'executor',
            # 'tags',
        )
        labels = {
            'name': _('Name'),
            'description': _('Description'),
            'status': _('Status'),
            'executor': _('Executor'),
            'tags': _('Tags'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['status'].widget.attrs.update({'class': 'form-control'})
        self.fields['executor'].widget.attrs.update({'class': 'form-control'})
        # self.fields['tags'].widget.attrs.update({'class': 'form-control'})
