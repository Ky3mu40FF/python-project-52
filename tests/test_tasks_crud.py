from django.db.utils import IntegrityError
import pytest
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


def test_should_create_task(db, status_1, simple_user_1) -> Task:
    task_name = 'Task name'
    task_description = 'Task description.'
    task = Task.objects.create(
        name = task_name,
        description = task_description,
        status = status_1,
        author = simple_user_1,
        executor = simple_user_1,
    )
    assert task.name == task_name
    assert task.description == task_description
    assert task.status == status_1
    assert task.author == simple_user_1
    assert task.executor == simple_user_1


def test_create_two_different_tasks_create(db, task_1, task_2):
    assert task_1 != task_2



def test_prevent_from_creating_task_without_name(db, status_1, simple_user_1):
    with pytest.raises(IntegrityError):
        task = Task.objects.create(
            name=None,
            description='Task description.',
            status=status_1,
            author=simple_user_1,
            executor=simple_user_1,
        )


def test_prevent_from_creating_task_without_author(db, status_1, simple_user_1):
    with pytest.raises(IntegrityError):
        task = Task.objects.create(
            name='Task name.',
            description='Task description.',
            status=status_1,
            author=None,
            executor=simple_user_1,
        )


def test_prevent_from_creating_task_without_status(db, status_1, simple_user_1):
    with pytest.raises(IntegrityError):
        task = Task.objects.create(
            name='Task name.',
            description='Task description.',
            status=None,
            author=simple_user_1,
            executor=simple_user_1,
        )
