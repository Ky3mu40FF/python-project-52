from django.urls import reverse_lazy
from task_manager.tasks.models import Task


def test_tasks_list_view(
    db,
    django_db_setup,
    client,
    task_model_test_fixtures,
    user_model_test_fixtures,
):
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )

    response = client.get(reverse_lazy('tasks'))

    assert response.status_code == 200
    assert next(filter(
        lambda template: template.name == 'tasks/list.html',
        response.templates
    ), False)
    # Check QuerySet
    assert len(response.context['tasks']) == Task.objects.count()
    assert set(response.context['tasks']) == set(Task.objects.all())
    # Check if view contains all neccessary links (create task and update and delete existing)
    assert '/tasks/create/' in str(response.content)
    for pk in range(1, Task.objects.count() + 1):
        assert f'/tasks/{pk}/update/' in str(response.content)
        assert f'/tasks/{pk}/delete/' in str(response.content)


def test_tasks_list_view_not_logged_in(db, django_db_setup, client):
    response = client.get(reverse_lazy('tasks'))

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('login')


def test_tasks_filter_by_status(
    db,
    django_db_setup,
    client,
    task_model_test_fixtures,
    user_model_test_fixtures,
):
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )

    response = client.get(
        reverse_lazy('tasks'),
        {'status': 1},
    )

    task1 = Task.objects.get(pk=1)
    task2 = Task.objects.get(pk=2)

    assert response.status_code == 200
    assert next(filter(
        lambda template: template.name == 'tasks/list.html',
        response.templates
    ), False)
    assert len(response.context['tasks']) == 1
    assert task1.name in str(response.content.decode('utf-8'))
    assert task2.name not in str(response.content.decode('utf-8'))


def test_tasks_filter_by_executor(
    db,
    django_db_setup,
    client,
    task_model_test_fixtures,
    user_model_test_fixtures,
):
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )

    response = client.get(
        reverse_lazy('tasks'),
        {'executor': 1},
    )

    task1 = Task.objects.get(pk=1)
    task2 = Task.objects.get(pk=2)

    assert response.status_code == 200
    assert next(filter(
        lambda template: template.name == 'tasks/list.html',
        response.templates
    ), False)
    assert len(response.context['tasks']) == 1
    assert task1.name not in str(response.content.decode('utf-8'))
    assert task2.name in str(response.content.decode('utf-8'))


def test_tasks_filter_by_label(
    db,
    django_db_setup,
    client,
    task_model_test_fixtures,
    user_model_test_fixtures,
):
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )

    response = client.get(
        reverse_lazy('tasks'),
        {'labels': 1},
    )

    task1 = Task.objects.get(pk=1)
    task2 = Task.objects.get(pk=2)

    assert response.status_code == 200
    assert next(filter(
        lambda template: template.name == 'tasks/list.html',
        response.templates
    ), False)
    assert len(response.context['tasks']) == 1
    assert task1.name in str(response.content.decode('utf-8'))
    assert task2.name not in str(response.content.decode('utf-8'))


def test_tasks_filter_own_tasks(
    db,
    django_db_setup,
    client,
    task_model_test_fixtures,
    user_model_test_fixtures,
):
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )

    response = client.get(
        reverse_lazy('tasks'),
        {'owned_by_user': 'on'},
    )

    task1 = Task.objects.get(pk=1)
    task2 = Task.objects.get(pk=2)

    assert response.status_code == 200
    assert next(filter(
        lambda template: template.name == 'tasks/list.html',
        response.templates
    ), False)
    assert len(response.context['tasks']) == 1
    assert task1.name not in str(response.content.decode('utf-8'))
    assert task2.name in str(response.content.decode('utf-8'))


def test_details_view(
    db,
    django_db_setup,
    client,
    task_model_test_fixtures,
    user_model_test_fixtures,
):
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )

    response = client.get(reverse_lazy('tasks_details', kwargs={'pk': 1}))

    task1 = Task.objects.get(pk=1)
    labels = task1.labels.all()

    assert response.status_code == 200
    assert next(filter(
        lambda template: template.name == 'tasks/details.html',
        response.templates
    ), False)
    assert task1.name in str(response.content.decode('utf-8'))
    assert task1.description in str(response.content.decode('utf-8'))
    assert task1.status.name in str(response.content.decode('utf-8'))
    assert task1.author.get_full_name() in str(response.content.decode('utf-8'))
    assert task1.executor.get_full_name() in str(response.content.decode('utf-8'))

    for label in labels:
        assert label.name in str(response.content.decode('utf-8'))


def test_details_view_not_logged_in(db, django_db_setup, client):
    response = client.get(reverse_lazy('tasks_details', kwargs={'pk': 1}))

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('login')


def test_tasks_create_view(
    db,
    django_db_setup,
    client,
    task_model_test_fixtures,
    user_model_test_fixtures,
):
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )

    response = client.get(reverse_lazy('tasks_create'))

    assert response.status_code == 200
    assert next(filter(lambda template: template.name == 'form.html', response.templates), False)


def test_tasks_create_view_not_logged_in(db, django_db_setup, client):
    response = client.get(reverse_lazy('tasks_create'))

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('login')


def test_tasks_update_view(
    db,
    django_db_setup,
    client,
    task_model_test_fixtures,
    user_model_test_fixtures,
):
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )

    response = client.get(reverse_lazy('tasks_update', kwargs={'pk': 1}))

    assert response.status_code == 200
    assert next(filter(lambda template: template.name == 'form.html', response.templates), False)


def test_tasks_update_view_not_logged_in(db, django_db_setup, client):
    response = client.get(reverse_lazy('tasks_update', kwargs={'pk': 1}))

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('login')


def test_tasks_delete_view(
    db,
    django_db_setup,
    client,
    task_model_test_fixtures,
    user_model_test_fixtures,
):
    user_data = user_model_test_fixtures['login']['user1']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )

    response = client.get(reverse_lazy('tasks_delete', kwargs={'pk': 2}))

    assert response.status_code == 200
    assert next(filter(
        lambda template: template.name == 'tasks/delete.html',
        response.templates
    ), False)


def test_tasks_delete_view_different_user(
    db,
    django_db_setup,
    client,
    task_model_test_fixtures,
    user_model_test_fixtures,
):
    user_data = user_model_test_fixtures['login']['user2']['auth_data'].copy()
    client.login(
        username=user_data['username'],
        password=user_data['password'],
    )

    response = client.get(reverse_lazy('tasks_delete', kwargs={'pk': 2}))

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('tasks')


def test_tasks_delete_view_not_logged_in(db, django_db_setup, client):
    response = client.get(reverse_lazy('tasks_delete', kwargs={'pk': 1}))

    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('login')
