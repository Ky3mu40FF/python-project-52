"""task_manager.views module."""
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Show index page."""

    template_name = 'index.html'
    extra_context = {
        'title': _('Task Manager'),
    }
