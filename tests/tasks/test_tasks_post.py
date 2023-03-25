from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
import pytest
from task_manager.tasks.models import Task


# https://docs.djangoproject.com/en/4.1/ref/urlresolvers/#django.urls.ResolverMatch

def test_create_valid_task(db, django_db_setup, client, task_model_test_fixtures, user_model_test_fixtures) -> None:
    task_data = task_model_test_fixtures['create']['valid'].copy()
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )
    tasks_count_before_creation = Task.objects.count()
    response = client.post(
        reverse_lazy('tasks_create'),
        data=task_data
    )

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('tasks')
    assert Task.objects.count() == tasks_count_before_creation+1
    assert Task.objects.last().name == task_data['name']


def test_create_missing_fields(db, django_db_setup, client, task_model_test_fixtures, user_model_test_fixtures) -> None:
    task_data = task_model_test_fixtures['create']['missing_fields'].copy()
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )
    tasks_count_before_creation = Task.objects.count()
    response = client.post(
        reverse_lazy('tasks_create'),
        data=task_data
    )

    errors = response.context['form'].errors
    error_help = _('This field is required.')

    assert 'name' in errors
    assert [error_help] == errors['name']

    assert response.status_code == 200
    assert Task.objects.count() == tasks_count_before_creation


def test_create_existing_task(db, django_db_setup, client, task_model_test_fixtures, user_model_test_fixtures) -> None:
    task_data = task_model_test_fixtures['create']['exists'].copy()
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )
    tasks_count_before_creation = Task.objects.count()
    response = client.post(
        reverse_lazy('tasks_create'),
        data=task_data
    )

    errors = response.context['form'].errors
    error_help = _('Task with this Name already exists.')

    assert 'name' in errors
    assert [error_help] == errors['name']

    assert response.status_code == 200
    assert Task.objects.count() == tasks_count_before_creation


def test_create_long_name(db, django_db_setup, client, task_model_test_fixtures, user_model_test_fixtures) -> None:
    task_data = task_model_test_fixtures['create']['valid'].copy()
    task_data['name'] = task_data['name'] * 100
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )
    tasks_count_before_creation = Task.objects.count()
    response = client.post(
        reverse_lazy('tasks_create'),
        data=task_data
    )

    errors = response.context['form'].errors
    error_help = _('Ensure this value has at most 100 characters (it has %s}).') % len(task_data["name"])

    assert 'name' in errors
    assert [error_help] == errors['name']

    assert response.status_code == 200
    assert Task.objects.count() == tasks_count_before_creation


def test_create_task_not_logged_in(db, django_db_setup, client, task_model_test_fixtures) -> None:
    task_data = task_model_test_fixtures['create']['valid'].copy()
    tasks_count_before_creation = Task.objects.count()
    response = client.post(
        reverse_lazy('tasks_create'),
        data=task_data
    )

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('login')
    assert Task.objects.count() != tasks_count_before_creation+1
    assert Task.objects.last().name != task_data['name']


def test_update_task_valid(db, django_db_setup, client, task_model_test_fixtures, user_model_test_fixtures) -> None:
    task_data = task_model_test_fixtures['update']['valid'].copy()
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )
    tasks_count_before_creation = Task.objects.count()
    response = client.post(
        reverse_lazy('tasks_update', kwargs={'pk': 1}),
        data=task_data
    )

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('tasks')
    assert Task.objects.count() == tasks_count_before_creation
    assert Task.objects.get(pk=1).name == task_data['name']
