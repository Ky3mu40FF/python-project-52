from django.db.models.deletion import ProtectedError
from django.db.utils import IntegrityError
import pytest
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


def test_create_status(db, django_db_setup, status_model_test_fixtures) -> None:
    status_data = status_model_test_fixtures['create']['valid'].copy()
    status = Status.objects.create(name=status_data['name'])

    assert isinstance(status, Status)
    assert Status.objects.filter(id=status.id).exists()
    assert status.__str__() == status_data['name']
    assert status.name == status_data['name']


def test_create_status_null_name(db, django_db_setup, status_model_test_fixtures) -> None:
    status_data = status_model_test_fixtures['create']['null_fields'].copy()

    with pytest.raises(IntegrityError):
        Status.objects.create(name=status_data['name'])


def test_create_status_existing_name(db, django_db_setup, status_model_test_fixtures) -> None:
    status_data = status_model_test_fixtures['create']['exists'].copy()
    with pytest.raises(IntegrityError):
        Status.objects.create(name=status_data['name'])
    

def test_delete_status_existing_not_associated_with_task(db, django_db_setup, status_model_test_fixtures) -> None:
    status_data = status_model_test_fixtures['delete']['valid'].copy()
    status = Status.objects.get(name=status_data['name'])
    status.delete()
    with pytest.raises(Status.DoesNotExist):
        Status.objects.get(name=status_data['name'])


def test_delete_status_not_existing(db, django_db_setup, status_model_test_fixtures) -> None:
    status_data = status_model_test_fixtures['delete']['not_exists'].copy()
    with pytest.raises(Status.DoesNotExist):
        status = Status.objects.get(name=status_data['name'])
        status.delete()


def test_delete_status_associated_with_task(db, django_db_setup, status_model_test_fixtures) -> None:
    status_data = status_model_test_fixtures['delete']['associated_with_task'].copy()
    status = Status.objects.get(name=status_data['name'])

    with pytest.raises(IntegrityError):
        status.delete()
