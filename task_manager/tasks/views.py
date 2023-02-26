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


class TestUserLoggedInAndOwnership(AccessMixin):
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
        if self.request.user.id != kwargs.get('author_id'):
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


class IndexView(LoginRequiredMixin, View):
    """Display list of all Task model instances (Authorized only)."""

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


class TaskDetailsView(LoginRequiredMixin, View):
    """Display Task model instance details (Authorized only)."""

    pass


class TaskCreateFormView(LoginRequiredMixin, View):
    """Display creation form of Task model instance (Authorized only)."""

    pass


class TaskUpdateFormView(LoginRequiredMixin, View):
    """Display updating form of Status model instance (Authorized only)."""

    pass


class TaskDeleteFormView(TestUserLoggedInAndOwnership, View):
    """Display deletion form of Status model instance (Only by author)."""

    pass

