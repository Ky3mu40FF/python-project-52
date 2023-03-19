# from django.db.models.deletion import ProtectedError
# from django.db.utils import IntegrityError
# from django.test import Client
# import pytest
# from task_manager.users.models import User


# def test_with_not_authenticated_client(client):
#     response = client.get('/labels/')
#     assert response.status_code == 403
#     response = client.get('/statuses/')
#     assert response.status_code == 403
#     response = client.get('/tasks/')
#     assert response.status_code == 403


# def test_with_authenticated_client(client, simple_user_1):
#     client.force_login(simple_user_1)
#     response = client.get('/labels/')
#     assert response.status_code == 200
#     response = client.get('/statuses/')
#     assert response.status_code == 200
#     response = client.get('/tasks/')
#     assert response.status_code == 200

