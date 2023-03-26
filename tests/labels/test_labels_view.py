from django.urls import reverse_lazy
from task_manager.labels.models import Label


def test_labels_list_view(
    db,
    django_db_setup,
    client,
    label_model_test_fixtures,
    user_model_test_fixtures,
):
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )

    response = client.get(reverse_lazy('labels'))

    assert response.status_code == 200
    assert next(filter(
            lambda template: template.name == 'labels/list.html',
            response.templates,
        ),
        False,
    )
    # Check QuerySet
    assert len(response.context['labels']) == Label.objects.count()
    assert set(response.context['labels']) == set(Label.objects.all())
    # Check if view contains all neccessary links (create label and update and delete existing)
    assert '/labels/create/' in str(response.content)
    for pk in range(1, Label.objects.count() + 1):
        assert f'/labels/{pk}/update/' in str(response.content)
        assert f'/labels/{pk}/delete/' in str(response.content)


def test_labels_list_view_not_logged_in(db, django_db_setup, client):
    response = client.get(reverse_lazy('labels'))

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('login')


def test_labels_create_view(
    db,
    django_db_setup,
    client,
    label_model_test_fixtures,
    user_model_test_fixtures,
):
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )

    response = client.get(reverse_lazy('labels_create'))

    assert response.status_code == 200
    assert next(filter(lambda template: template.name == 'form.html', response.templates), False)


def test_labels_create_view_not_logged_in(db, django_db_setup, client):
    response = client.get(reverse_lazy('labels_create'))

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('login')


def test_labels_update_view(
    db,
    django_db_setup,
    client,
    label_model_test_fixtures,
    user_model_test_fixtures,
):
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )

    response = client.get(reverse_lazy('labels_update', kwargs={'pk': 1}))

    assert response.status_code == 200
    assert next(filter(lambda template: template.name == 'form.html', response.templates), False)


def test_labels_update_view_not_logged_in(db, django_db_setup, client):
    response = client.get(reverse_lazy('labels_update', kwargs={'pk': 1}))

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('login')


def test_labels_delete_view(
    db,
    django_db_setup,
    client,
    label_model_test_fixtures,
    user_model_test_fixtures,
):
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )

    response = client.get(reverse_lazy('labels_delete', kwargs={'pk': 1}))

    assert response.status_code == 200
    assert next(filter(
            lambda template: template.name == 'labels/delete.html',
            response.templates,
        ),
        False,
    )


def test_labels_delete_view_not_logged_in(db, django_db_setup, client):
    response = client.get(reverse_lazy('labels_delete', kwargs={'pk': 1}))

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('login')
