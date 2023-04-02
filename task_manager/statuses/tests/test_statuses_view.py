from django.urls import reverse_lazy
from task_manager.statuses.models import Status


def test_statuses_list_view(
    db,
    django_db_setup,
    client,
    status_model_test_fixtures,
    user_model_test_fixtures,
):
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )

    response = client.get(reverse_lazy('statuses'))

    assert response.status_code == 200
    assert next(filter(
        lambda template: template.name == 'statuses/list.html',
        response.templates,
    ), False)

    # Check QuerySet
    assert len(response.context['statuses']) == Status.objects.count()
    assert set(response.context['statuses']) == set(Status.objects.all())
    # Check if view contains all neccessary links (create status and update and delete existing)
    assert '/statuses/create/' in str(response.content)
    for pk in range(1, Status.objects.count() + 1):
        assert f'/statuses/{pk}/update/' in str(response.content)
        assert f'/statuses/{pk}/delete/' in str(response.content)


def test_statuses_list_view_not_logged_in(db, django_db_setup, client):
    response = client.get(reverse_lazy('statuses'))

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('login')


def test_statuses_create_view(
    db,
    django_db_setup,
    client,
    status_model_test_fixtures,
    user_model_test_fixtures,
):
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )

    response = client.get(reverse_lazy('statuses_create'))

    assert response.status_code == 200
    assert next(filter(lambda template: template.name == 'form.html', response.templates), False)


def test_statuses_create_view_not_logged_in(db, django_db_setup, client):
    response = client.get(reverse_lazy('statuses_create'))

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('login')


def test_statuses_update_view(
    db,
    django_db_setup,
    client,
    status_model_test_fixtures,
    user_model_test_fixtures,
):
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )
    status_pk = 3
    response = client.get(reverse_lazy('statuses_update', kwargs={'pk': status_pk}))

    assert response.status_code == 200
    assert next(filter(lambda template: template.name == 'form.html', response.templates), False)


def test_statuses_update_view_not_logged_in(db, django_db_setup, client):
    status_pk = 3
    response = client.get(reverse_lazy('statuses_update', kwargs={'pk': status_pk}))

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('login')


def test_statuses_delete_view(
    db,
    django_db_setup,
    client,
    status_model_test_fixtures,
    user_model_test_fixtures,
):
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )
    status_pk = 3

    response = client.get(reverse_lazy('statuses_delete', kwargs={'pk': status_pk}))

    assert response.status_code == 200
    assert next(filter(
        lambda template: template.name == 'statuses/delete.html',
        response.templates,
    ), False)


def test_statuses_delete_view_not_logged_in(db, django_db_setup, client):
    status_pk = 3
    response = client.get(reverse_lazy('statuses_delete', kwargs={'pk': status_pk}))

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('login')
