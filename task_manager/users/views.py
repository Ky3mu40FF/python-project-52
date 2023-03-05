"""task_manager - users app - views module with users app view classes."""
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View
from task_manager.users.forms import (
    CustomAuthenticationForm,
    CustomUserChangeForm,
    CustomUserCreationForm,
)
from task_manager.users.models import User


class TestUserLoggedInAndOwnership(AccessMixin):
    """Custom mixin to check user permissions.

    Check if user accessing his own resources
    or if he is logged in.
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
        if self.request.user.id != kwargs.get('id'):
            messages.error(
                self.request,
                _('You do not have permission for this action.'),
            )
            return redirect('users')

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


class IndexView(View):
    """Display list of all User model instances."""

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """Render page with users list.

        Returns:
            Render page with users list.
        """
        users = User.objects.all()
        return render(request, 'users/index.html', context={
            'users': users,
        })


class UserCreationFormView(View):
    """Display creation form of User model instance."""

    def get(self, request, *args, **kwargs):
        """Render page with user creation form.

        Returns:
            Render page with user registration form.
        """
        form = CustomUserCreationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        """Create new user.

        Create new user and redirect to Log In page if adding was successful,
        or render register view with validation errors.

        Returns:
            Redirect to user login page for success,
            render user register page with errors otherwise.
        """
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.save()
            return redirect('users_login')
        for field in form.errors:
            form[field].field.widget.attrs['class'] += ' is-invalid'
        return render(request, 'users/register.html', {'form': form})


class UserChangeFormView(TestUserLoggedInAndOwnership, View):
    """Display change form for User model instance."""

    def get(self, request, *args, **kwargs):
        """Render page with user change form.

        Returns:
            Render page with user change form.
        """
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        form = CustomUserChangeForm(instance=user)
        return render(request, 'users/update.html', {
            'form': form,
            'user_id': user_id,
        })

    def post(self, request, *args, **kwargs):
        """Change user.

        Change user and redirect to Users list page if changin was successful,
        or render User change view with validation errors.

        Returns:
            Redirect to Users list page
            or render page with User change form.
        """
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.save()
            return redirect('users')
        for field in form.errors:
            form[field].field.widget.attrs['class'] += ' is-invalid'
        return render(request, 'users/update.html', {
            'form': form,
            'user_id': user_id,
        })


class UserDeleteFormView(TestUserLoggedInAndOwnership, View):
    """Display deletion form for User model instance."""

    def get(self, request, *args, **kwargs):
        """Render page with user deletion form.

        Returns:
            Render page with user deletion form.
        """
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        return render(request, 'users/delete.html', {
            'user_id': user.id,
            'user_full_name': user.full_name,
        })

    def post(self, request, *args, **kwargs):
        """Delete user.

        Delete user and redirect to Users list page.

        Returns:
            Redirect to Users list page.
        """
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        if user:
            if user.created_tasks or user.executing_tasks:
                messages.error(
                    self.request,
                    _('You cannot delete user associated with tasks.'),
                )
                return redirect('users')
            user.delete()
            return redirect('homepage')


class UserAuthenticationFormView(View):
    """Display authentication form."""

    def get(self, request, *args, **kwargs):
        """Render page with user authentication form.

        Returns:
            Render page with user authentication form.
        """
        form = CustomAuthenticationForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        """Log in user.

        Logging in user and redirect to Home page
        if authentication was successful,
        or render log in page with errors messages displayed.

        Returns:
            Redirect to Users list page.
        """
        form = CustomAuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, _('Successfully Logged In!'))
                return redirect('homepage')
        return render(request, 'users/login.html', {'form': form})


class UserLogOutView(View):
    """View for user loggin out."""

    def post(self, request, *args, **kwargs):
        """Log out user.

        Returns:
            Redirect to Home page.
        """
        logout(request)
        messages.success(request, _('Successfully Logged Out!'))
        return redirect('homepage')
