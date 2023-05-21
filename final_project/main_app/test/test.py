from django.test import Client
import pytest


@pytest.mark.django_db
def test_main():
    client = Client()
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_requires_login():
    client = Client()
    response = client.get('/companies')
    assert response.status_code == 302
    assert response.url == '/accounts/login/?next=/companies'
