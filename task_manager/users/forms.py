"""task_manager.users.forms module."""
from django.contrib.auth.forms import UserCreationForm
from task_manager.users.models import User


class CustomUserForm(UserCreationForm):
    """Custom creation and update form for custom User model."""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )
