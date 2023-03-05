from django.db.models.deletion import ProtectedError
from django.db.utils import IntegrityError
import pytest
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


def test_should_create_simple_user(db: None) -> None:
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


def test_should_create_super_user(db: None) -> None:
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


def test_two_different_users_create(simple_user_1: User, simple_user_2: User):
    assert simple_user_1 != simple_user_2


def test_two_different_super_users_create(super_user_1: User, super_user_2: User):
    assert super_user_1 != super_user_2


def test_two_simple_users_same_username_integrity_error(simple_user_1: User):
    with pytest.raises(IntegrityError):
        User.objects.create_user(
            username=simple_user_1.username,
            password="some_password",
        )


def test_simple_user_and_super_user_same_username_integrity_error(super_user_1: User):
    with pytest.raises(IntegrityError):
        User.objects.create_user(
            username=super_user_1.username,
            password="some_password",
        )


def test_update_user(simple_user_1: User):
    simple_user_1.first_name = "Albert"
    simple_user_1.is_active = False
    simple_user_1.save()
    simple_user_1_from_db = User.objects.get(username=simple_user_1.username)
    assert simple_user_1_from_db.first_name == "Albert"
    assert simple_user_1_from_db.is_active is False


def test_change_username_to_not_existed(simple_user_1: User):
    new_username = 'definitely_not_Exists'
    simple_user_1.username = new_username
    simple_user_1.save()
    simple_user_1_from_db = User.objects.get(username=new_username)
    assert simple_user_1_from_db.username == new_username


def test_change_username_to_existed(simple_user_1: User, simple_user_2: User):
    simple_user_1.username = simple_user_2.username
    with pytest.raises(IntegrityError):
        simple_user_1.save()


def test_delete_user(simple_user_1: User):
    username = simple_user_1.username
    simple_user_1.delete()
    assert not User.objects.filter(username=username).exists()


def test_prevent_from_deleting_user_associated_with_tasks(
    simple_user_1: User,
    simple_user_2: User,
    simple_user_3: User,
    status_1: Status,
    status_2: Status,
    task_1: Task,
    task_2: Task
):
    # simple_user_1 is author and executor for task_1 
    # and author for task_2.
    with pytest.raises(ProtectedError):
        simple_user_1.delete()
    # simple_user_2 is executor for task_2.
    with pytest.raises(ProtectedError):
        simple_user_2.delete()
    # simple_user_3 is not associated with any tasks.
    assert simple_user_3.delete()
