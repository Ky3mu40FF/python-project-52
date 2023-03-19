from django.db.models.deletion import ProtectedError
from django.db.utils import IntegrityError
import pytest
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


def test_create_label(db, django_db_setup, label_model_test_fixtures) -> None:
    label_data = label_model_test_fixtures['create']['valid'].copy()
    label = Label.objects.create(name=label_data['name'])

    assert isinstance(label, Label)
    assert Label.objects.filter(id=label.id).exists()
    assert label.__str__() == label_data['name']
    assert label.name == label_data['name']


def test_create_label_null_name(db, django_db_setup, label_model_test_fixtures) -> None:
    label_data = label_model_test_fixtures['create']['null_fields'].copy()

    with pytest.raises(IntegrityError):
        Label.objects.create(name=label_data['name'])


def test_create_label_existing_name(db, django_db_setup, label_model_test_fixtures) -> None:
    label_data = label_model_test_fixtures['create']['exists'].copy()
    with pytest.raises(IntegrityError):
        Label.objects.create(name=label_data['name'])
    

def test_delete_label_existing_not_associated_with_task(db, django_db_setup, label_model_test_fixtures) -> None:
    label_data = label_model_test_fixtures['delete']['valid'].copy()
    label = Label.objects.get(name=label_data['name'])
    label.delete()
    with pytest.raises(Label.DoesNotExist):
        Label.objects.get(name=label_data['name'])


def test_delete_label_not_existing(db, django_db_setup, label_model_test_fixtures) -> None:
    label_data = label_model_test_fixtures['delete']['not_exists'].copy()
    with pytest.raises(Label.DoesNotExist):
        label = Label.objects.get(name=label_data['name'])
        label.delete()


def test_delete_label_associated_with_task(db, django_db_setup, label_model_test_fixtures) -> None:
    label_data = label_model_test_fixtures['delete']['associated_with_task'].copy()
    label = Label.objects.get(name=label_data['name'])

    with pytest.raises(IntegrityError):
        label.delete()
