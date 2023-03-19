from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.deletion import ProtectedError
from django.db.utils import IntegrityError
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
    # assert response.resolver_match.url_name == reverse_lazy('labels_create')
    assert response['Location'] == reverse_lazy('labels')
    assert Label.objects.count() == labels_count_before_creation+1
    assert Label.objects.last().name == label_data['name']


def test_create_label_unauthorized(db, django_db_setup, client, label_model_test_fixtures) -> None:
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
