import json
import os

import pytest
from django.core.management import call_command
from django.utils.translation import activate


@pytest.fixture(autouse=True)
def set_default_language():
    activate('ru-ru')


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'task_manager/fixtures/task_manager_data.json')


@pytest.fixture()
def label_model_test_fixtures(request):
    file_path = os.path.join('task_manager/fixtures', 'test_label.json')
    with open(file_path, mode='r') as fixture_file:
        fixture = json.load(fixture_file)
    return fixture


@pytest.fixture()
def user_model_test_fixtures(request):
    file_path = os.path.join('task_manager/fixtures', 'test_user.json')
    with open(file_path, mode='r') as fixture_file:
        fixture = json.load(fixture_file)
    return fixture


@pytest.fixture()
def status_model_test_fixtures(request):
    file_path = os.path.join('task_manager/fixtures', 'test_status.json')
    with open(file_path, mode='r') as fixture_file:
        fixture = json.load(fixture_file)
    return fixture


@pytest.fixture()
def task_model_test_fixtures(request):
    file_path = os.path.join('task_manager/fixtures', 'test_task.json')
    with open(file_path, mode='r') as fixture_file:
        fixture = json.load(fixture_file)
    return fixture
