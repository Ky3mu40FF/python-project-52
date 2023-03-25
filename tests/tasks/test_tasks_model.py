from django.db.models.deletion import ProtectedError
from django.db.utils import IntegrityError
import pytest
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


def test_create_task(db, django_db_setup, task_model_test_fixtures) -> None:
    task_data = task_model_test_fixtures['create']['valid'].copy()
    task = Task.objects.create(
        name=task_data['name'],
        description=task_data['description'],
        author_id=1,
        executor_id=task_data['executor'],
        status_id=task_data['status'],
    )

    assert isinstance(task, Task)
    assert Task.objects.filter(id=task.id).exists()
    assert task.__str__() == task_data['name']
    assert isinstance(task.author, User)
    assert isinstance(task.executor, User)
    assert isinstance(task.status, Status)
