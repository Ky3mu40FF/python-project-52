from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from task_manager.statuses.models import Status


def test_create_valid_status(
    db,
    django_db_setup,
    client,
    status_model_test_fixtures,
    user_model_test_fixtures,
) -> None:
    status_data = status_model_test_fixtures['create']['valid'].copy()
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )
    statuses_count_before_creation = Status.objects.count()
    response = client.post(
        reverse_lazy('statuses_create'),
        data=status_data,
    )

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('statuses')
    assert Status.objects.count() == statuses_count_before_creation + 1
    assert Status.objects.last().name == status_data['name']


def test_create_missing_fields(
    db,
    django_db_setup,
    client,
    status_model_test_fixtures,
    user_model_test_fixtures,
) -> None:
    status_data = status_model_test_fixtures['create']['missing_fields'].copy()
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )
    statuses_count_before_creation = Status.objects.count()
    response = client.post(
        reverse_lazy('statuses_create'),
        data=status_data,
    )

    errors = response.context['form'].errors
    error_help = _('This field is required.')

    assert 'name' in errors
    assert [error_help] == errors['name']

    assert response.status_code == 200
    assert Status.objects.count() == statuses_count_before_creation


def test_create_existing_status(
    db,
    django_db_setup,
    client,
    status_model_test_fixtures,
    user_model_test_fixtures,
) -> None:
    status_data = status_model_test_fixtures['create']['exists'].copy()
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )
    statuses_count_before_creation = Status.objects.count()
    response = client.post(
        reverse_lazy('statuses_create'),
        data=status_data,
    )

    errors = response.context['form'].errors
    error_help = _('Status with this Name already exists.')

    assert 'name' in errors
    assert [error_help] == errors['name']

    assert response.status_code == 200
    assert Status.objects.count() == statuses_count_before_creation


def test_create_long_name(
    db,
    django_db_setup,
    client,
    status_model_test_fixtures,
    user_model_test_fixtures,
) -> None:
    status_data = status_model_test_fixtures['create']['valid'].copy()
    status_data['name'] = status_data['name'] * 100
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )
    statuses_count_before_creation = Status.objects.count()
    response = client.post(
        reverse_lazy('statuses_create'),
        data=status_data,
    )

    errors = response.context['form'].errors
    error_help = _(
        'Ensure this value has at most 100 characters (it has %s}).'
    ) % len(status_data["name"])

    assert 'name' in errors
    assert [error_help] == errors['name']

    assert response.status_code == 200
    assert Status.objects.count() == statuses_count_before_creation


def test_create_status_not_logged_in(
    db,
    django_db_setup,
    client,
    status_model_test_fixtures,
) -> None:
    status_data = status_model_test_fixtures['create']['valid'].copy()
    statuses_count_before_creation = Status.objects.count()
    response = client.post(
        reverse_lazy('statuses_create'),
        data=status_data,
    )

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('login')
    assert Status.objects.count() != statuses_count_before_creation + 1
    assert Status.objects.last().name != status_data['name']


def test_update_status_valid(
    db,
    django_db_setup,
    client,
    status_model_test_fixtures,
    user_model_test_fixtures,
) -> None:
    status_data = status_model_test_fixtures['update']['valid'].copy()
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )
    statuses_count_before_creation = Status.objects.count()
    status_pk = 3
    response = client.post(
        reverse_lazy('statuses_update', kwargs={'pk': status_pk}),
        data=status_data,
    )

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('statuses')
    assert Status.objects.count() == statuses_count_before_creation
    assert Status.objects.get(pk=status_pk).name == status_data['name']
