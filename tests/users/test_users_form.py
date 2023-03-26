from task_manager.users.forms import CustomUserForm
from task_manager.users.models import User


def test_create_user(db, django_db_setup, user_model_test_fixtures) -> None:
    user_data = user_model_test_fixtures['create']['valid'].copy()
    form = CustomUserForm(data=user_data)

    assert form.is_valid()


def test_create_user_with_empty_name(db, django_db_setup, user_model_test_fixtures) -> None:
    user_data = user_model_test_fixtures['create']['missing_fields'].copy()
    form = CustomUserForm(data=user_data)

    assert not form.is_valid()


def test_create_user_with_existing_name(db, django_db_setup, user_model_test_fixtures) -> None:
    user_data = user_model_test_fixtures['create']['exists'].copy()
    form = CustomUserForm(data=user_data)

    assert not form.is_valid()


def test_update_user(db, django_db_setup, user_model_test_fixtures) -> None:
    user_data = user_model_test_fixtures['update']['valid'].copy()
    user = User.objects.get(pk=1)
    form = CustomUserForm(data=user_data, instance=user)

    assert form.is_valid()
