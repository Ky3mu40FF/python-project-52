from django.db.utils import IntegrityError
import pytest

from task_manager.users.models import User


def test_should_create_simple_user(simple_user_one) -> None:
    user = User.objects.create_user(
        username="TestUser",
        password="TestPassword",
        last_name="Wesker",
    )
    assert user.username == 'TestUser'
    assert User.check_password(user, 'TestPassword')
    assert user.first_name == ''
    assert user.last_name == 'Wesker'
    assert user.is_active is True
    assert user.is_staff is False
    assert user.is_superuser is False


def test_should_create_super_user(db) -> None:
    user = User.objects.create_superuser(
        username="TestSuperUser",
        password="TestPassword",
        first_name="Claire",
    )
    assert user.username == 'TestSuperUser'
    assert User.check_password(user, 'TestPassword')
    assert user.first_name == 'Claire'
    assert user.last_name == ''
    assert user.is_active is True
    assert user.is_staff is True
    assert user.is_superuser is True


def test_two_different_users_create(simple_user_one, simple_user_two):
    assert simple_user_one != simple_user_two


def test_two_different_super_users_create(super_user_one, super_user_two):
    assert super_user_one != super_user_two


def test_two_simple_users_same_username_integrity_error(simple_user_one):
    with pytest.raises(IntegrityError):
        User.objects.create_user(
            username=simple_user_one.username,
            password="some_password",
        )


def test_simple_user_and_super_user_same_username_integrity_error(super_user_one):
    with pytest.raises(IntegrityError):
        User.objects.create_user(
            username=super_user_one.username,
            password="some_password",
        )


def test_update_user(simple_user_one):
    simple_user_one.first_name = "Albert"
    simple_user_one.is_active = False
    simple_user_one.save()
    simple_user_one_from_db = User.objects.get(username=simple_user_one.username)
    assert simple_user_one_from_db.first_name == "Albert"
    assert simple_user_one_from_db.is_active is False


def test_change_username_to_not_existed(simple_user_one):
    new_username = 'definitely_not_Exists'
    simple_user_one.username = new_username
    simple_user_one.save()
    simple_user_one_from_db = User.objects.get(username=new_username)
    assert simple_user_one_from_db.username == new_username


def test_change_username_to_existed(simple_user_one, simple_user_two):
    simple_user_one.username = simple_user_two.username
    with pytest.raises(IntegrityError):
        simple_user_one.save()


def test_delete_user(simple_user_one):
    username = simple_user_one.username
    simple_user_one.delete()
    assert not User.objects.filter(username=username).exists()
