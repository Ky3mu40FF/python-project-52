"""task_manager - labels - views module."""
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from task_manager.labels.forms import LabelCreateForm, LabelUpdateForm
from task_manager.labels.models import Label
from task_manager.mixins import AuthRequiredMixin, DeleteProtectionMixin


class LabelsListView(AuthRequiredMixin, ListView):
    """Show all labels.

    Authorization required.
    """

    template_name = 'labels/list.html'
    model = Label
    context_object_name = 'labels'
    extra_context = {
        'title': _('Labels'),
    }


class LabelCreateFormView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    """Create new label.

    Authorization required.
    """

    template_name = 'form.html'
    model = Label
    form_class = LabelCreateForm
    success_url = reverse_lazy('labels')
    success_message = _('Label is successfully created!')
    extra_context = {
        'title': _('Label creation'),
        'button_text': _('Create'),
    }


class LabelUpdateFormView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update selected label.

    Authorization required.
    """

    template_name = 'form.html'
    model = Label
    form_class = LabelUpdateForm
    success_url = reverse_lazy('labels')
    success_message = _('Label is successfully updated!')
    extra_context = {
        'title': _('Label updating'),
        'button_text': _('Update'),
    }


class LabelDeleteFormView(
    AuthRequiredMixin,
    DeleteProtectionMixin,
    SuccessMessageMixin,
    DeleteView,
):
    """Delete selected label.

    Authorization required.
    """

    template_name = 'labels/delete.html'
    model = Label
    success_url = reverse_lazy('labels')
    success_message = _('Label is successfully deleted!')
    protected_url = reverse_lazy('labels')
    protected_message = _('You cannot delete the label assiciated with task.')
    extra_context = {
        'title': _('Label deletion'),
        'button_text': _('Yes, delete'),
    }
