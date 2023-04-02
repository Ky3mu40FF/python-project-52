import pytest
from django.db.utils import IntegrityError
from task_manager.users.models import User


def test_create_user(db, django_db_setup, user_model_test_fixtures) -> None:
    user_data = user_model_test_fixtures['create']['valid'].copy()
    user = User.objects.create(
        username=user_data['username'],
        first_name=user_data['first_name'],
        last_name=user_data['last_name'],
    )
    user.set_password(user_data['password1'])
    full_name = user_data['first_name'] + ' ' + user_data['last_name']

    assert isinstance(user, User)
    assert User.objects.filter(id=user.id).exists()
    assert user.__str__() == full_name
    assert user.username == user_data['username']
    assert user.check_password(user_data['password1'])


def test_create_user_null_fields(db, django_db_setup, user_model_test_fixtures) -> None:
    user_data = user_model_test_fixtures['create']['null_fields'].copy()

    with pytest.raises(IntegrityError):
        User.objects.create(
            username=user_data['username'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
        )


def test_create_user_existing_username(db, django_db_setup, user_model_test_fixtures) -> None:
    user_data = user_model_test_fixtures['create']['exists'].copy()
    with pytest.raises(IntegrityError):
        User.objects.create(
            username=user_data['username'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
        )
