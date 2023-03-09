import pytest
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


@pytest.fixture
def simple_user_1(db) -> User:
    return User.objects.create_user(
        username='Zombie_Slayer',
        password='NoThanksBro',
        first_name='Leon',
        last_name='Kennedy',
    )


@pytest.fixture
def simple_user_2(db) -> User:
    return User.objects.create_user(
        username='Rock_Slayer',
        password='RedfieldsBloodline',
        first_name='Chris',
        last_name='Redfield',
    )


@pytest.fixture
def simple_user_3(db) -> User:
    return User.objects.create_user(
        username='Whisker',
        password='GlobalSaturation',
        first_name='Albert',
        last_name='Wesker',
    )


@pytest.fixture
def super_user_1(db) -> User:
    return User.objects.create_user(
        username='TestSuperUserOne',
        password='TestPassword',
        first_name='Admin',
        last_name='Adminov',
    )


@pytest.fixture
def super_user_2(db) -> User:
    return User.objects.create_user(
        username='TestSuperUser-Two',
        password='TestPassword',
        first_name='Кристофер',
        last_name='Нолан',
    )


@pytest.fixture
def status_1(db) -> Status:
    return Status.objects.create(name='New')


@pytest.fixture
def status_2(db) -> Status:
    return Status.objects.create(name='In Progress')


@pytest.fixture
def status_3_not_used(db) -> Status:
    return Status.objects.create(name='Not in use')


@pytest.fixture
def label_1(db) -> Label:
    return Label.objects.create(
        name='B.O.W.',
    )


@pytest.fixture
def label_2(db) -> Label:
    return Label.objects.create(
        name='Bloodline',
    )


@pytest.fixture
def label_3_not_used(db) -> Label:
    return Label.objects.create(
        name='Not Used',
    )


@pytest.fixture
def task_1(db, simple_user_1, status_1, label_1) -> Task:
    task = Task.objects.create(
        name='Спасти Эшли',
        description='Её нашли в испанской деревушке. Нужно её найти.',
        status=status_1,
        author=simple_user_1,
        executor=simple_user_1,
    )
    task.labels.add(label_1)
    task.save()
    return task


@pytest.fixture
def task_2(db, simple_user_1, simple_user_2, status_2, label_1, label_2) -> Task:
    task = Task.objects.create(
        name='Continue Redfield Bloodline',
        description='You want my sister? You can have her! I left everything you need together at my place Now you just have to *@%^ her',
        status=status_2,
        author=simple_user_1,
        executor=simple_user_2,
    )
    task.labels.add(label_1, label_2)
    task.save()
    return task
