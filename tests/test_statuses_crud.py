from django.db.utils import IntegrityError
import pytest
from task_manager.statuses.models import Status

def test_should_create_status(db) -> None:
    status = Status.objects.create(name='Новая')
    assert status.name == 'Новая'
    assert Status.objects.filter(id=status.id).exists()


def test_two_different_statuses_create(status1, status2) -> None:
    assert status1 != status2


def test_two_statuses_same_name_integrity_error(status1) -> None:
    with pytest.raises(IntegrityError):
        status2 = Status.objects.create(name=status1.name)


def test_null_name(db) -> None:
    with pytest.raises(IntegrityError):
        status = Status.objects.create(name=None)


def test_update_status(status1) -> None:
    status1_previous_name = status1.name
    status1_new_name = 'Завершено'
    status1.name = status1_new_name
    status1.save()
    status1_from_db = Status.objects.get(id=status1.id)
    assert status1_from_db.name != status1_previous_name
    assert status1_from_db.name == status1_new_name
    assert Status.objects.filter(name=status1_new_name).exists()
    assert not Status.objects.filter(name=status1_previous_name).exists()


def test_delete_status(status1) -> None:
    status1_id = status1.id
    status1.delete()
    assert not Status.objects.filter(id=status1_id).exists()