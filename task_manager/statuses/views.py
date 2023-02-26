from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View
from task_manager.statuses.forms import (
    StatusCreateForm,
    StatusUpdateForm,
)
from task_manager.statuses.models import Status


class IndexView(LoginRequiredMixin, View):
    """Display list of all Status model instances."""

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """Render page with statuses list.

        Returns:
            Render page with statuses list.
        """
        statuses = Status.objects.all()
        return render(request, 'statuses/index.html', context={
            'statuses': statuses,
        })


class StatusCreateFormView(LoginRequiredMixin, View):
    """Display creation form of Status model instance."""

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """Render page with status creation form.
        
        Returns:
            Render page with status creation form.
        """
        form = StatusCreateForm()
        return render(request, 'statuses/create.html', {'form': form})

    def post(self, request, *args, **kwargs) -> HttpResponse:
        """Create new status.
        
        Returns:
            Redirect to statuses list page
            or render page wit status creation form with added erros.
        """
        form = StatusCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('The status is successfully created!'))
            return redirect('statuses')
        for field in form.errors:
            form[field].field.widget.attrs['class'] += ' is-invalid'
        return render(request, 'statuses/create.html', {'form': form})


class StatusUpdateFormView(LoginRequiredMixin, View):
    """Display updating form of Status model instance."""

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """Render page with status updating form.
        
        Returns:
            Render page with status updating form.
        """
        status_id = kwargs.get('id')
        status = Status.objects.get(id=status_id)
        form = StatusUpdateForm(instance=status)
        return render(request, 'statuses/update.html', {
            'form': form,
            'status_id': status_id,
        })

    def post(self, request, *args, **kwargs) -> HttpResponse:
        """Update selected status.
        
        Returns:
            Redirect to statuses list page
            or render page wit status updating form with added erros.
        """
        status_id = kwargs.get('id')
        status = Status.objects.get(id=status_id)
        form = StatusUpdateForm(data=request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, _('The status is successfully updated!'))
            return redirect('statuses')
        for field in form.errors:
            form[field].field.widget.attrs['class'] += ' is-invalid'
        return render(request, 'statuses/update.html', {
            'form': form,
            'status_id': status_id,
        })


class StatusDeleteFormView(LoginRequiredMixin, View):
    """Display delition form of Status model instance."""

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """Render page with status delition form.
        
        Returns:
            Render page with status delition form.
        """
        status_id = kwargs.get('id')
        status = Status.objects.get(id=status_id)
        return render(request, 'statuses/delete.html', {
            'status_id': status_id,
            'status_name': status.name,
        })

    def post(self, request, *args, **kwargs) -> HttpResponse:
        """Delete selected status.
        
        Returns:
            Redirect to statuses list page
        """
        status_id = kwargs.get('id')
        status = Status.objects.get(id=status_id)
        if status:
            status.delete()
            messages.success(request, _('The status is successfully deleted!'))
            return redirect('statuses')
