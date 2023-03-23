import pytest
from task_manager.statuses.forms import StatusCreateForm, StatusUpdateForm

def test_create_status(db, django_db_setup, status_model_test_fixtures) -> None:
    status_data = status_model_test_fixtures['create']['valid'].copy()
    form = StatusCreateForm(data=status_data)

    assert form.is_valid()


def test_create_status_with_empty_name(db, django_db_setup, status_model_test_fixtures) -> None:
    status_data = status_model_test_fixtures['create']['missing_fields'].copy()
    form = StatusCreateForm(data=status_data)

    assert not form.is_valid()


def test_create_status_with_existing_name(db, django_db_setup, status_model_test_fixtures) -> None:
    status_data = status_model_test_fixtures['create']['exists'].copy()
    form = StatusCreateForm(data=status_data)

    assert not form.is_valid()


def test_update_status(db, django_db_setup, status_model_test_fixtures) -> None:
    status_data = status_model_test_fixtures['update']['valid'].copy()
    form = StatusUpdateForm(data=status_data)

    assert form.is_valid()
