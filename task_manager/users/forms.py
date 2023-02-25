"""task_manager.users.forms module."""
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    UserCreationForm,
)
from django.utils.translation import gettext_lazy as _
from task_manager.users.models import User


class CustomAuthenticationForm(AuthenticationForm):
    """Custom authentication form for custom User model."""

    class Meta(AuthenticationForm):
        model = User
        fields = ('username',)
    
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})


class CustomUserCreationForm(UserCreationForm):
    """Custom creation form for custom User model."""

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'first_name', 'last_name',)
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class CustomUserChangeForm(UserChangeForm):
    """Custom change form for custom User model."""

    password1 = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta(UserChangeForm):
        model = User
        fields = ('username', 'first_name', 'last_name',)
    
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'class': 'form-control'})

    # https://docs.djangoproject.com/en/4.1/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other
    def clean(self):
        cleaned_data = super(CustomUserChangeForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            # raise forms.ValidationError("password and confirm_password does not match")
            self.add_error('password2', _("The two password fields didn’t match."))
        
        return cleaned_data
