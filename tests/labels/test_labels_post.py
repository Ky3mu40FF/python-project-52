from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
import pytest
from task_manager.labels.models import Label


# https://docs.djangoproject.com/en/4.1/ref/urlresolvers/#django.urls.ResolverMatch

def test_create_valid_label(db, django_db_setup, client, label_model_test_fixtures, user_model_test_fixtures) -> None:
    label_data = label_model_test_fixtures['create']['valid'].copy()
    user_data = user_model_test_fixtures['login']['simple1'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )
    labels_count_before_creation = Label.objects.count()
    response = client.post(
        reverse_lazy('labels_create'),
        data=label_data
    )

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('labels')
    assert Label.objects.count() == labels_count_before_creation+1
    assert Label.objects.last().name == label_data['name']


def test_create_missing_fields(db, django_db_setup, client, label_model_test_fixtures, user_model_test_fixtures) -> None:
    label_data = label_model_test_fixtures['create']['missing_fields'].copy()
    user_data = user_model_test_fixtures['login']['simple1'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )
    labels_count_before_creation = Label.objects.count()
    response = client.post(
        reverse_lazy('labels_create'),
        data=label_data
    )

    errors = response.context['form'].errors
    error_help = _('This field is required.')

    assert 'name' in errors
    assert [error_help] == errors['name']

    assert response.status_code == 200
    assert Label.objects.count() == labels_count_before_creation


def test_create_existing_label(db, django_db_setup, client, label_model_test_fixtures, user_model_test_fixtures) -> None:
    label_data = label_model_test_fixtures['create']['exists'].copy()
    user_data = user_model_test_fixtures['login']['simple1'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )
    labels_count_before_creation = Label.objects.count()
    response = client.post(
        reverse_lazy('labels_create'),
        data=label_data
    )

    errors = response.context['form'].errors
    error_help = _('Label with this Name already exists.')

    assert 'name' in errors
    assert [error_help] == errors['name']

    assert response.status_code == 200
    assert Label.objects.count() == labels_count_before_creation


def test_create_long_name(db, django_db_setup, client, label_model_test_fixtures, user_model_test_fixtures) -> None:
    label_data = label_model_test_fixtures['create']['valid'].copy()
    label_data['name'] = label_data['name'] * 100
    user_data = user_model_test_fixtures['login']['simple1'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )
    labels_count_before_creation = Label.objects.count()
    response = client.post(
        reverse_lazy('labels_create'),
        data=label_data
    )

    errors = response.context['form'].errors
    error_help = _('Ensure this value has at most 100 characters ' f'(it has {len(label_data["name"])}).')

    assert 'name' in errors
    assert [error_help] == errors['name']

    assert response.status_code == 200
    assert Label.objects.count() == labels_count_before_creation


def test_create_label_not_logged_in(db, django_db_setup, client, label_model_test_fixtures) -> None:
    label_data = label_model_test_fixtures['create']['valid'].copy()
    labels_count_before_creation = Label.objects.count()
    response = client.post(
        reverse_lazy('labels_create'),
        data=label_data
    )

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('login')
    assert Label.objects.count() != labels_count_before_creation+1
    assert Label.objects.last().name != label_data['name']


def test_update_label_valid(db, django_db_setup, client, label_model_test_fixtures, user_model_test_fixtures) -> None:
    label_data = label_model_test_fixtures['update']['valid'].copy()
    user_data = user_model_test_fixtures['login']['simple1'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )
    labels_count_before_creation = Label.objects.count()
    response = client.post(
        reverse_lazy('labels_update', kwargs={'pk': 1}),
        data=label_data
    )

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('labels')
    assert Label.objects.count() == labels_count_before_creation
    assert Label.objects.get(pk=1).name == label_data['name']
