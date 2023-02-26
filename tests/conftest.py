import pytest
from task_manager.statuses.models import Status
from task_manager.users.models import User


@pytest.fixture
def simple_user_one(db) -> User:
    return User.objects.create_user(
        username='simple_user_one',
        password='simple_password',
        first_name='Leon',
        last_name='Kennedy',
    )


@pytest.fixture
def simple_user_two(db) -> User:
    return User.objects.create_user(
        username='Simple_User_Two',
        password='TestPassword',
    )


@pytest.fixture
def super_user_one(db) -> User:
    return User.objects.create_user(
        username='TestSuperUserOne',
        password='TestPassword',
        first_name='Admin',
        last_name='Adminov',
    )


@pytest.fixture
def super_user_two(db) -> User:
    return User.objects.create_user(
        username='TestSuperUser-Two',
        password='TestPassword',
        first_name='Кристофер',
        last_name='Нолан',
    )


@pytest.fixture
def status1(db) -> Status:
    return Status.objects.create(name='Новая')


@pytest.fixture
def status2(db) -> Status:
    return Status.objects.create(name='В работе')
