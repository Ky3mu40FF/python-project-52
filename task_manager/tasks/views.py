"""task_manager - tasks app - views module with tasks app view classes."""
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View
from task_manager.tasks.forms import (
    TaskCreateForm,
    TaskUpdateForm,
)
from task_manager.tasks.models import Task


class IndexView(LoginRequiredMixin, View):
    """Display list of all Task model instances."""

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """Render page with tasks list.
        
        Returns:
            Render page with tasks list.
        """
        tasks = Task.objects.select_related('status', 'author', 'executor').only(
            'name',
            'description',
            'status__name',
            'author__first_name',
            'author__last_name',
            'executor__first_name',
            'executor__last_name',
        )
        return render(request, 'tasks/index.html', context={
            'tasks': tasks,
        })
