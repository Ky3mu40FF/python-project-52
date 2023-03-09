from django.db.models.deletion import ProtectedError
from django.db.utils import IntegrityError
import pytest
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


def test_should_create_label(db) -> None:
    label = Label.objects.create(name='New')
    assert label.name == 'New'
    assert Label.objects.filter(id=label.id).exists()


def test_two_different_labeles_create(label_1, label_2) -> None:
    assert label_1 != label_2


def test_two_labeles_same_name_integrity_error(label_1) -> None:
    with pytest.raises(IntegrityError):
        label_2 = Label.objects.create(name=label_1.name)


def test_null_name(db) -> None:
    with pytest.raises(IntegrityError):
        label = Label.objects.create(name=None)


def test_update_label(label_1) -> None:
    label_1_previous_name = label_1.name
    label_1_new_name = 'Tyrant'
    label_1.name = label_1_new_name
    label_1.save()
    label_1_from_db = Label.objects.get(id=label_1.id)
    assert label_1_from_db.name != label_1_previous_name
    assert label_1_from_db.name == label_1_new_name
    assert Label.objects.filter(name=label_1_new_name).exists()
    assert not Label.objects.filter(name=label_1_previous_name).exists()


def test_delete_label(label_1) -> None:
    label_1_id = label_1.id
    label_1.delete()
    assert not Label.objects.filter(id=label_1_id).exists()


def test_prevent_from_deleting_label_associated_with_tasks(
    label_1: Label,
    label_3_not_used: Label,
    task_1: Task,
):
    # label_1 is associated with task_1.
    with pytest.raises(ProtectedError):
        assert label_1.delete()
    # simple_user_3 is not associated with any tasks.
    assert label_3_not_used.delete()

