"""task_manager.views module."""
# task_manager/views.py
from django.shortcuts import render


def index(request):
    """Render Home page.

    Args:
        request(Any): Request params.

    Returns:
        Render Home page.
    """
    return render(request, 'index.html')
