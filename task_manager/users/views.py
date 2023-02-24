from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from .models import User
from .forms import CustomAuthenticationForm, CustomUserCreationForm, CustomUserChangeForm

class IndexView(View):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, 'users/index.html', context={
            'users': users,
        })

class UserCreationFormView(View):

    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        return render(request, 'users/register.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.save()
            return HttpResponseRedirect(reverse('users_login'))
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
            return render(request, 'users/register.html', {'form': form})


class UserChangeFormView(View):

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        if request.user.id == user_id:
            user = User.objects.get(id=user_id)
            form = CustomUserChangeForm(instance=user)
            return render(request, 'users/update.html', {
                'form': form,
                'user_id': user_id
            })
        else:
            messages.add_message(request, messages.ERROR, 'You can not update different user!')
            return HttpResponseRedirect(reverse('users'))

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        if request.user.id == user_id:
            user = User.objects.get(id=user_id)
            form = CustomUserChangeForm(request.POST, instance=user)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data.get('password1'))
                user.save()
                return HttpResponseRedirect(reverse('users'))
            else:
                for field in form.errors:
                    form[field].field.widget.attrs['class'] += ' is-invalid'
                return render(request, 'users/update.html', {
                    'form': form,
                    'user_id': user_id
                })
        else:
            messages.add_message(request, messages.ERROR, 'You can not update different user!')
            return HttpResponseRedirect(reverse('users'))

class UserDeleteFormView(View):

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        if request.user.id == user_id:
            user = User.objects.get(id=user_id)
            return render(request, 'users/delete.html', {
                'user_id': user.id,
                'user_full_name': user.full_name,
            })
        else:
            messages.add_message(request, messages.ERROR, 'You can not delete different user!')
            return HttpResponseRedirect(reverse('users'))

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        if request.user.id == user_id:
            user = User.objects.get(id=user_id)
            if user:
                user.delete()
                return HttpResponseRedirect(reverse('homepage'))
        else:
            messages.add_message(request, messages.ERROR, 'You can not delete different user!')
            return HttpResponseRedirect(reverse('users'))

class UserAuthenticationFormView(View):

    def get(self, request, *args, **kwargs):
        form = CustomAuthenticationForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomAuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Successfully Logged In!')
                return HttpResponseRedirect(reverse('homepage'))
            else:
                return render(request, 'users/login.html', {'form': form})
        else:
            return render(request, 'users/login.html', {'form': form})

class UserLogOutView(View):

    def post(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('homepage'))
