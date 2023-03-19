from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView, DeleteView, ListView, UpdateView,
)
from task_manager.mixins import AuthRequiredMixin, DeleteProtectionMixin
from task_manager.statuses.forms import StatusCreateForm, StatusUpdateForm
from task_manager.statuses.models import Status


class StatusesListView(AuthRequiredMixin, ListView):
    """Show all statuses.
    
    Authorization required.
    """

    template_name = 'statuses/list.html'
    model = Status
    context_object_name = 'statuses'
    extra_context = {
        'title': _('Statuses'),
    }


class StatusCreateFormView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    """Create new status.
    
    Authorization required.
    """

    template_name = 'form.html'
    model = Status
    form_class = StatusCreateForm
    success_url = reverse_lazy('statuses')
    success_message = _('Status is successfully created!')
    extra_context = {
        'title': _('Status creation'),
        'button_text': _('Create'),
    }
    

class StatusUpdateFormView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update selected status.
    
    Authorization required.
    """

    template_name = 'form.html'
    model = Status
    form_class = StatusUpdateForm
    success_url = reverse_lazy('statuses')
    success_message = _('Status is successfully updated!')
    extra_context = {
        'title': _('Status updating'),
        'button_text': _('Update'),
    }


class StatusDeleteFormView(AuthRequiredMixin, DeleteProtectionMixin, SuccessMessageMixin, DeleteView):
    """Delete selected status.
    
    Authorization required.
    If status is associated with task - it cannot be deleted.
    """

    template_name = 'statuses/delete.html'
    model = Status
    success_url = reverse_lazy('statuses')
    success_message = _('Status is successfully deleted!')
    protected_url = reverse_lazy('statuses')
    protected_message = _('You cannot delete the status associated with task.')
    extra_context = {
        'title': _('Status deletion'),
        'button_text': _('Yes, delete'),
    }
