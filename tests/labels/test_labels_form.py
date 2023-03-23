import pytest
from task_manager.labels.forms import LabelCreateForm, LabelUpdateForm

def test_create_label(db, django_db_setup, label_model_test_fixtures) -> None:
    label_data = label_model_test_fixtures['create']['valid'].copy()
    form = LabelCreateForm(data=label_data)

    assert form.is_valid()


def test_create_label_with_empty_name(db, django_db_setup, label_model_test_fixtures) -> None:
    label_data = label_model_test_fixtures['create']['missing_fields'].copy()
    form = LabelCreateForm(data=label_data)

    assert not form.is_valid()


def test_create_label_with_existing_name(db, django_db_setup, label_model_test_fixtures) -> None:
    label_data = label_model_test_fixtures['create']['exists'].copy()
    form = LabelCreateForm(data=label_data)

    assert not form.is_valid()


def test_update_label(db, django_db_setup, label_model_test_fixtures) -> None:
    label_data = label_model_test_fixtures['update']['valid'].copy()
    form = LabelUpdateForm(data=label_data)

    assert form.is_valid()
