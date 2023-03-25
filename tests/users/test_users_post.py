from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
import pytest
from task_manager.users.models import User


# https://docs.djangoproject.com/en/4.1/ref/urlresolvers/#django.urls.ResolverMatch

def test_create_valid_user(db, django_db_setup, client, user_model_test_fixtures) -> None:
    user_data = user_model_test_fixtures['create']['valid'].copy()
    user_login_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_login_data['username'],
        password=user_login_data['password'],
    )
    users_count_before_creation = User.objects.count()
    response = client.post(
        reverse_lazy('users_create'),
        data=user_data
    )

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('login')
    assert User.objects.count() == users_count_before_creation+1
    assert User.objects.last().username == user_data['username']


def test_create_missing_fields(db, django_db_setup, client, user_model_test_fixtures) -> None:
    user_data = user_model_test_fixtures['create']['missing_fields'].copy()
    user_login_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_login_data['username'],
        password=user_login_data['password'],
    )
    users_count_before_creation = User.objects.count()
    response = client.post(
        reverse_lazy('users_create'),
        data=user_data
    )

    errors = response.context['form'].errors
    error_help = _('This field is required.')

    assert 'username' in errors
    assert [error_help] == errors['username']

    assert response.status_code == 200
    assert User.objects.count() == users_count_before_creation


def test_create_existing_user(db, django_db_setup, client, user_model_test_fixtures) -> None:
    user_data = user_model_test_fixtures['create']['exists'].copy()
    user_login_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_login_data['username'],
        password=user_login_data['password'],
    )
    users_count_before_creation = User.objects.count()
    response = client.post(
        reverse_lazy('users_create'),
        data=user_data
    )

    errors = response.context['form'].errors
    error_help = _('User with this Username already exists.')

    assert 'username' in errors
    assert [error_help] == errors['username']

    assert response.status_code == 200
    assert User.objects.count() == users_count_before_creation


def test_create_long_name(db, django_db_setup, client, user_model_test_fixtures) -> None:
    user_data = user_model_test_fixtures['create']['valid'].copy()
    user_data['username'] = user_data['username'] * 100
    user_login_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_login_data['username'],
        password=user_login_data['password'],
    )
    users_count_before_creation = User.objects.count()
    response = client.post(
        reverse_lazy('users_create'),
        data=user_data
    )

    errors = response.context['form'].errors
    error_help = _('Ensure this value has at most 100 characters ' f'(it has {len(user_data["username"])}).')

    assert 'username' in errors
    assert [error_help] == errors['username']

    assert response.status_code == 200
    assert User.objects.count() == users_count_before_creation


def test_create_user_not_logged_in(db, django_db_setup, client, user_model_test_fixtures) -> None:
    user_data = user_model_test_fixtures['create']['valid'].copy()
    users_count_before_creation = User.objects.count()
    response = client.post(
        reverse_lazy('users_create'),
        data=user_data
    )

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('login')
    assert User.objects.count() == users_count_before_creation+1
    assert User.objects.last().username == user_data['username']


def test_update_user_valid(db, django_db_setup, client, user_model_test_fixtures) -> None:
    user_data = user_model_test_fixtures['update']['valid'].copy()
    user_login_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_login_data['username'],
        password=user_login_data['password'],
    )
    users_count_before_creation = User.objects.count()
    response = client.post(
        reverse_lazy('users_update', kwargs={'pk': 1}),
        data=user_data
    )

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('users')
    assert User.objects.count() == users_count_before_creation
    # assert User.objects.get(pk=1).username == user_data['username']
