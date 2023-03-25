import pytest
from task_manager.tasks.forms import TaskCreateForm, TaskUpdateForm
from task_manager.tasks.models import Task

def test_create_task(db, django_db_setup, task_model_test_fixtures) -> None:
    task_data = task_model_test_fixtures['create']['valid'].copy()
    form = TaskCreateForm(data=task_data)
    assert form.is_valid()


def test_create_task_with_empty_fields(db, django_db_setup, task_model_test_fixtures) -> None:
    task_data = task_model_test_fixtures['create']['missing_fields'].copy()
    form = TaskCreateForm(data=task_data)

    assert not form.is_valid()

def test_update_task(db, django_db_setup, task_model_test_fixtures) -> None:
    task_data = task_model_test_fixtures['update']['valid'].copy()
    task = Task.objects.get(pk=1)
    form = TaskUpdateForm(data=task_data, instance=task)
    assert form.is_valid()
