from django.urls import reverse_lazy
from task_manager.users.models import User


def test_users_list_view(db, django_db_setup, client, user_model_test_fixtures):
    """
    Test users list view.
    Authentication is not required.
    """
    response = client.get(reverse_lazy('users'))

    assert response.status_code == 200
    assert next(filter(
        lambda template: template.name == 'users/list.html',
        response.templates
    ), False)
    # Check QuerySet
    assert len(response.context['users']) == User.objects.count()
    assert set(response.context['users']) == set(User.objects.all())
    # Check if view contains all neccessary links (create user and update and delete existing)
    assert '/users/create/' in str(response.content)
    for pk in range(1, User.objects.count() + 1):
        assert f'/users/{pk}/update/' in str(response.content)
        assert f'/users/{pk}/delete/' in str(response.content)


def test_users_create_view(db, django_db_setup, client, user_model_test_fixtures):
    """
    Test users creation view.
    Authentication is not required.
    """
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )

    response = client.get(reverse_lazy('users_create'))

    assert response.status_code == 200
    assert next(filter(lambda template: template.name == 'form.html', response.templates), False)


def test_users_update_view(db, django_db_setup, client, user_model_test_fixtures):
    """
    Test users updating view.
    Authentication is required.
    User can update only himself.
    Situation: user1 is trying update himself.
    """
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )

    response = client.get(reverse_lazy('users_update', kwargs={
        'pk': user_model_test_fixtures['login']['user1']['pk'],
    }))

    assert response.status_code == 200
    assert next(filter(lambda template: template.name == 'form.html', response.templates), False)


def test_users_update_view_different_user(db, django_db_setup, client, user_model_test_fixtures):
    """
    Test users updating view.
    Authentication is required.
    User can update only himself.
    Situation: user2 is trying to update another user.
    """
    user_data = user_model_test_fixtures['login']['user2']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )

    response = client.get(reverse_lazy('users_update', kwargs={'pk': 1}))

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('users')


def test_users_update_view_not_logged_in(db, django_db_setup, client):
    """
    Test users updating view.
    Authentication is required.
    User can update only himself.
    Situation: anonymous user is trying to update user.
    """
    response = client.get(reverse_lazy('users_update', kwargs={'pk': 1}))

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('login')


def test_users_delete_view(db, django_db_setup, client, user_model_test_fixtures):
    """
    Test users deletion view.
    Authentication is required.
    User can delete only himself.
    Situation: user1 is trying delete himself.
    """
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )

    response = client.get(reverse_lazy('users_delete', kwargs={
        'pk': user_model_test_fixtures['login']['user1']['pk'],
    }))

    assert response.status_code == 200
    assert next(filter(
        lambda template: template.name == 'users/delete.html',
        response.templates
    ), False)


def test_users_delete_view_different_user(db, django_db_setup, client, user_model_test_fixtures):
    """
    Test users deletion view.
    Authentication is required.
    User can delete only himself.
    Situation: user2 is trying delete another user.
    """
    user_data = user_model_test_fixtures['login']['user2']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )

    response = client.get(reverse_lazy('users_delete', kwargs={'pk': 1}))

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('users')


def test_users_delete_view_not_logged_in(db, django_db_setup, client):
    """
    Test users deletion view.
    Authentication is required.
    User can delete only himself.
    Situation: anonymous user is trying delete another user.
    """
    response = client.get(reverse_lazy('users_delete', kwargs={'pk': 1}))

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('login')
