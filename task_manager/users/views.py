"""task_manager - users app - views module with users app view classes."""
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView, DeleteView, ListView, UpdateView,
)
from task_manager.mixins import AuthRequiredMixin, UserPermissionMixin, DeleteProtectionMixin
from task_manager.users.forms import (
    CustomUserForm,
)
from task_manager.users.models import User


class UsersListView(ListView):
    """
    Show all users.
    """

    template_name = 'users/list.html'    
    model = User
    context_object_name = 'users'
    extra_context = {
        'title': _('Users'),
    }


class UserCreationFormView(SuccessMessageMixin, CreateView):
    """
    Register new user.
    """

    template_name = 'form.html'
    model = User
    form_class = CustomUserForm
    success_url = reverse_lazy('login')
    success_message = _('User is successfully registered!')
    extra_context = {
        'title': _('User registration'),
        'button_text': _('Register'),
    }


class UserUpdateFormView(AuthRequiredMixin, UserPermissionMixin, UpdateView):
    """
    Update user.

    Authorization required.
    Only user can update himself.
    """

    template_name = 'form.html'
    model = User
    form_class = CustomUserForm
    success_url = reverse_lazy('users')
    success_message = _('User is successfully updated!')
    permission_url = reverse_lazy('users')
    permission_message = _('You cannot update another users.')
    extra_context = {
        'title': _('User updating'),
        'button_text': _('Update'),
    }


class UserDeleteFormView(AuthRequiredMixin, UserPermissionMixin,
                         DeleteProtectionMixin, DeleteView):
    """
    Delete user.

    Authorization required.
    If user is associated with task - it cannot be deleted.
    Only user can delete himself.
    """

    template_name = 'users/delete.html'
    model = User
    success_url = reverse_lazy('users')
    success_message = _('User is successfully deleted!')
    permission_url = reverse_lazy('users')
    permission_message = _('Only user can delete himself.')
    protected_url = reverse_lazy('users')
    protected_message = _('You cannot delete the user associated with task.')
    extra_context = {
        'title': _('User deletion'),
        'button_text': _('Yes, delete'),
    }


class UserAuthenticationFormView(SuccessMessageMixin, LoginView):
    """
    Log In user.
    """

    template_name = 'form.html'
    form_class = AuthenticationForm
    next_page = reverse_lazy('homepage')
    success_message = _('You are logged in!')
    extra_context = {
        'title': _('Login'),
        'button_text': _('Login'),
    }


class UserLogOutView(LogoutView):
    """
    Log Out user.
    """

    next_page = reverse_lazy('homepage')
    success_message = _('You are logged out!')
