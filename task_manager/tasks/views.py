"""task_manager - tasks app - views module with tasks app view classes."""
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView, DeleteView, DetailView, UpdateView,
)
from django_filters.views import FilterView
from task_manager.mixins import AuthRequiredMixin, AuthorDeletionMixin
from task_manager.tasks.filter import TaskFilter
from task_manager.tasks.forms import TaskCreateForm, TaskUpdateForm
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TasksListView(AuthRequiredMixin, FilterView):
    """Show filtered list of tasks.
    
    Authorization required.
    """

    template_name = 'tasks/list.html'
    model = Task
    filterset_class = TaskFilter
    context_object_name = 'tasks'
    extra_context = {
        'title': _('Tasks'),
        'button_text': _('Show'),
    }


class TaskDetailsView(AuthRequiredMixin, DetailView):
    """Show task details.
    
    Authorization required.
    """

    template_name = 'tasks/details.html'
    model = Task
    context_object_name = 'task'
    extra_context = {
        'title': _('Task details'),
    }


class TaskCreateFormView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    """Create new task.
    
    Authorization required.
    """

    template_name = 'form.html'
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy('tasks')
    success_message = _('Task is successfully created!')
    extra_context = {
        'title': _('Task creation'),
        'button_text': _('Create'),
    }

    def form_valid(self, form):
        """
        Set current user as the task's author.
        """
        user = self.request.user
        form.instance.author = User.objects.get(pk=user.pk)
        return super().form_valid(form)


class TaskUpdateFormView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update selected task.

    Authorization required.
    """

    template_name = 'form.html'
    model = Task
    form_class = TaskUpdateForm
    success_url = reverse_lazy('tasks')
    success_message = _('Task is successfully updated!')
    extra_context = {
        'title': _('Task updating'),
        'button_text': _('Update'),
    }


class TaskDeleteFormView(AuthRequiredMixin, AuthorDeletionMixin, SuccessMessageMixin, DeleteView):
    """Delete selected task.
    
    Authorization required.
    Only author can delete task.
    """

    template_name = 'tasks/delete.html'
    model = Task
    success_url = reverse_lazy('tasks')
    success_message = _('Task is successfully deleted!')
    author_url = reverse_lazy('tasks')
    author_message = _('Only authors can delete their tasks.')
    extra_context = {
        'title': _('Task deletion'),
        'button_text': _('Yes, delete'),
    }
