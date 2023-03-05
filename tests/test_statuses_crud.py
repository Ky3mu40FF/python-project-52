from django.db.models.deletion import ProtectedError
from django.db.utils import IntegrityError
import pytest
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


def test_should_create_status(db) -> None:
    status = Status.objects.create(name='Новая')
    assert status.name == 'Новая'
    assert Status.objects.filter(id=status.id).exists()


def test_two_different_statuses_create(status_1, status_2) -> None:
    assert status_1 != status_2


def test_two_statuses_same_name_integrity_error(status_1) -> None:
    with pytest.raises(IntegrityError):
        status_2 = Status.objects.create(name=status_1.name)


def test_null_name(db) -> None:
    with pytest.raises(IntegrityError):
        status = Status.objects.create(name=None)


def test_update_status(status_1) -> None:
    status_1_previous_name = status_1.name
    status_1_new_name = 'Завершено'
    status_1.name = status_1_new_name
    status_1.save()
    status_1_from_db = Status.objects.get(id=status_1.id)
    assert status_1_from_db.name != status_1_previous_name
    assert status_1_from_db.name == status_1_new_name
    assert Status.objects.filter(name=status_1_new_name).exists()
    assert not Status.objects.filter(name=status_1_previous_name).exists()


def test_delete_status(status_1) -> None:
    status_1_id = status_1.id
    status_1.delete()
    assert not Status.objects.filter(id=status_1_id).exists()


def test_prevent_from_deleting_user_associated_with_tasks(
    status_1: Status,
    status_3_not_used: Status,
    task_1: Task,
):
    # status_1 is associated with task_1.
    with pytest.raises(ProtectedError):
        status_1.delete()
    # simple_user_3 is not associated with any tasks.
    assert status_3_not_used.delete()
