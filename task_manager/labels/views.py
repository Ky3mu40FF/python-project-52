from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View
from task_manager.labels.forms import (
    LabelCreateForm,
    LabelUpdateForm,
)
from task_manager.labels.models import Label


class IndexView(LoginRequiredMixin, View):
    """Display list of all Label model instances."""

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """Render page with statuses list.
        
        Returns:
            Render page with labels list.
        """
        labels = Label.objects.all()
        return render(request, 'labels/index.html', context={
            'labels': labels,
        })


class LabelCreateFormView(LoginRequiredMixin, View):
    """Display creation form of Label model instance."""

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """Render page with label creation form.
        
        Returns:
            Render page with label creation form.
        """
        form = LabelCreateForm()
        return render(request, 'labels/create.html', {'form': form})

    def post(self, request, *args, **kwargs) -> HttpResponse:
        """Create new label.
        
        Returns:
            Redirect to labels list page
            or render page wit label creation form with added erros.
        """
        form = LabelCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('The label is successfully created!'))
            return redirect('labels')
        for field in form.errors:
            form[field].field.widget.attrs['class'] += ' is-invalid'
        return render(request, 'labels/create.html', {'form': form})


class LabelUpdateFormView(LoginRequiredMixin, View):
    """Display updating form of Label model instance."""

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """Render page with label updating form.
        
        Returns:
            Render page with label updating form.
        """
        label_id = kwargs.get('id')
        label = Label.objects.get(id=label_id)
        form = LabelUpdateForm(instance=label)
        return render(request, 'labels/update.html', {
            'form': form,
            'label_id': label_id,
        })

    def post(self, request, *args, **kwargs) -> HttpResponse:
        """Update selected label.
        
        Returns:
            Redirect to labels list page
            or render page wit label updating form with added erros.
        """
        label_id = kwargs.get('id')
        label = Label.objects.get(id=label_id)
        form = LabelUpdateForm(data=request.POST, instance=label)
        if form.is_valid():
            form.save()
            messages.success(request, _('The label is successfully updated!'))
            return redirect('labels')
        for field in form.errors:
            form[field].field.widget.attrs['class'] += ' is-invalid'
        return render(request, 'labels/update.html', {
            'form': form,
            'label_id': label_id,
        })


class LabelDeleteFormView(LoginRequiredMixin, View):
    """Display deletion form of Label model instance."""

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """Render page with label deletion form.
        
        Returns:
            Render page with label deletion form.
        """
        label_id = kwargs.get('id')
        label = Label.objects.get(id=label_id)
        return render(request, 'labels/delete.html', {
            'label_id': label_id,
            'label_name': label.name,
        })

    def post(self, request, *args, **kwargs) -> HttpResponse:
        """Delete selected label.
        
        Returns:
            Redirect to labels list page
        """
        label_id = kwargs.get('id')
        label = Label.objects.get(id=label_id)
        if label:
            if label.task_set.all():
                messages.error(
                    self.request,
                    _('You cannot delete label associated with tasks.'),
                )
                return redirect('labels')
            label.delete()
            messages.success(request, _('The label is successfully deleted!'))
            return redirect('labels')
