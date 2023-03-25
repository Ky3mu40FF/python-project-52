"""task_manager.tasks.filter module."""
from django import forms
from django.utils.translation import gettext_lazy as _
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskFilter(FilterSet):
    """Task filter by 'executor', 'status', 'labels' and ownage."""

    executor = ModelChoiceFilter(
        label=_('Executor'),
        queryset=User.objects.all(),
        widget=forms.Select,
    )
    status = ModelChoiceFilter(
        label=_('Status'),
        queryset=Status.objects.all(),
        widget=forms.Select,
    )
    labels = ModelChoiceFilter(
        label=_('Labels'),
        queryset=Label.objects.all(),
        widget=forms.Select,
    )
    owned_by_user = BooleanFilter(
        label=_('Only your tasks'),
        method='filter_user_owned',
        widget=forms.CheckboxInput,
    )

    def filter_user_owned(self, queryset, name, value):
        """
        Get tasks which author is current user.

        Returns:
            (QuerySet): Filtered tasks.
        """
        if value:
            user = getattr(self.request, 'user', None)
            return queryset.filter(author=user)
        return queryset

    class Meta:
        model = Task
        fields = [
            'status',
            'executor',
        ]
