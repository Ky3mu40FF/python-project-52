"""task_manager - tasks app - views module with tasks app view classes."""
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView,
    UpdateView,
)
from django_filters.views import FilterView
from task_manager.tasks.filter import TaskFilter
from task_manager.tasks.forms import (
    TaskCreateForm,
    TaskUpdateForm,
)
from task_manager.tasks.models import Task


class TestUserLoggedInAndOwnershipMixin(AccessMixin):
    """Custom mixin to check user permissions.

    Check if user accessing his own resources
    and if he is logged in.
    """

    def dispatch(self, request, *args, **kwargs):
        """AccessMixin dispatch overrided method.

        Check for ownership and authorization.

        Returns:
            Redirect to log in page if user is not authenticated,
            or redirect to users list page with error message if
            user have no permission to do current action,
            pass otherwise.
        """
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        
        task_id = kwargs.get('id')
        task_author_id = Task.objects.select_related('author').only('author__id').get(id=task_id).author_id
        if self.request.user.id != task_author_id:
            messages.error(
                self.request,
                _('You do not have permission for this action.'),
            )
            return redirect('tasks')

        # Checks pass, let http method handlers process the request
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        """AccessMixin handle_no_permission overrided method.

        Returns:
            Redirect to log in page with error message.
        """
        messages.error(
            self.request,
            _('You are not authorized. Please Log In.'),
        )
        return redirect('users_login')


class IndexView(LoginRequiredMixin, FilterView):
    """Display list of all Task model instances (Authorized only)."""

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """Render page with tasks list.
        
        Returns:
            Render page with tasks list.
        """
        tasks = Task.objects.select_related('status', 'author', 'executor').only(
            'name',
            'status__name',
            'author__first_name',
            'author__last_name',
            'executor__first_name',
            'executor__last_name',
        )
        filter = TaskFilter(request=request, data=request.GET, queryset=tasks)
        return render(request, 'tasks/index.html', context={
            'filter': filter,
        })


class TaskDetailsView(LoginRequiredMixin, DetailView):
    """Display Task model instance details (Authorized only)."""

    def get(self, request, *args, **kwargs):
        """Render page with details of Task model instance.

        Returns:
            Render page with details of Task model instance.
        """
        task_id = kwargs.get('id')
        task = Task.objects.select_related(
            'status',
            'author',
            'executor'
        ).only(
            'name',
            'description',
            'status__name',
            'author__first_name',
            'author__last_name',
            'executor__first_name',
            'executor__last_name',
            'labels__name',
        ).get(id=task_id)
        return render(request, 'tasks/details.html', {'task': task})


class TaskCreateFormView(LoginRequiredMixin, CreateView):
    """Display creation form of Task model instance (Authorized only)."""

    def get(self, request, *args, **kwargs):
        """Render page with task creation form.

        Returns:
            Render page with task creation form.
        """
        form = TaskCreateForm()
        return render(request, 'tasks/create.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        """Create new task.
        
        Returns:
            Redirect tp tasks list page
            or render page with task creation form with added errors.
        """
        form = TaskCreateForm(data=request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author_id = request.user.id
            task.save()
            messages.success(request, _('The task is successfully created!'))
            return redirect('tasks')
        for field in form.errors:
            if form[field].field.widget.attrs.get('class', None):
                form[field].field.widget.attrs['class'] += ' is-invalid'
        return render(request, 'tasks/create.html', {'form': form})


class TaskUpdateFormView(LoginRequiredMixin, UpdateView):
    """Display updating form of Status model instance (Authorized only)."""

    def get(self, request, *args, **kwargs):
        """Render page with task update form.
        
        Returns:
            Render page with status update form.
        """
        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)
        form = TaskUpdateForm(instance=task)
        return render(request, 'tasks/update.html', {
            'task_id': task_id,
            'form': form,
        })
    
    def post(self, request, *args, **kwargs):
        """Update selected task.
        
        Returns:
            Redirect to tasks list page if update was successful
            or render page with task update form with added errors otherwise.
        """
        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)
        form = TaskUpdateForm(data=request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, _('The task is successfully updated!'))
            return redirect('tasks')
        for field in form.errors:
            form[field].field.widget.attrs['class'] += ' is-invalid'
        return render(request, 'tasks/update.html', {
            'task_id': task_id,
            'form': form,
        })


class TaskDeleteFormView(TestUserLoggedInAndOwnershipMixin, DeleteView):
    """Display deletion form of Status model instance (Only by author)."""

    def get(self, request, *args, **kwargs):
        """Render page with task deletion form.
        
        Returns:
            Render page with status deletion form.
        """
        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)
        return render(request, 'tasks/delete.html', {
            'task_id': task_id,
            'task_name': task.name,
        })

    def post(self, request, *args, **kwargs):
        """Delete selected task.
        
        Returns:
            Redirect to tasks list page.
        """
        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)
        if task:
            task.delete()
            messages.success(request, _('The task is successfully deleted!'))
            return redirect('tasks')
