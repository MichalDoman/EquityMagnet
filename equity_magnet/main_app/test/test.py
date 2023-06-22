import pytest
from django.contrib.auth.models import User

from main_app.utils.general_utils import SORTING_NAMES


@pytest.mark.django_db
def test_home_view(client, companies):
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_company_list_view(client, companies):
    response = client.get("/companies/")
    assert response.status_code == 200
    assert len(response.context['page_obj']) == len(companies)
    assert response.context['page_obj'][0] == companies[0]


@pytest.mark.django_db
def test_company_list_filtering(client, companies):
    response = client.get("/companies/?phrase=company_1&market_cap=")
    assert response.status_code == 200
    assert len(response.context['page_obj']) == 1
    assert response.context['page_obj'][0] == companies[0]

    response = client.get("/companies/?phrase=&market_cap=3")
    assert response.status_code == 200
    assert len(response.context['page_obj']) == 1
    assert response.context['page_obj'][0] == companies[-1]


@pytest.mark.django_db
def test_company_list_sorting(client, companies):
    for sort in SORTING_NAMES:
        response = client.get(f"/companies/?phrase=&exchanges=1&market_cap=&sort_by={sort}")
        assert response.status_code == 200

        if sort[0] == "-":
            assert response.context['page_obj'][0] == companies[-1]
        else:
            assert response.context['page_obj'][0] == companies[0]


# def test_company_details_view(client, company):
#     response = client.get(f"/company-details/{company.pk}")
#     assert response.status_code == 200
#     assert response.context['company'] == company


@pytest.mark.django_db
def test_favorite_company_list_view(client, user, companies, favorite_companies):
    response = client.get("/watchlist/")
    assert len(response.context['companies']) == 0

    client.login(username="test_user", password="test")

    response = client.get("/watchlist/")
    assert response.status_code == 200
    assert len(response.context['companies']) == len(favorite_companies)
    assert response.context['companies'][0] == companies[0]


@pytest.mark.django_db
def test_company_evaluations_list_view(client, user, companies, evaluations):
    client.login(username="test_user", password="test")
    response = client.get("/evaluation-list/")

    assert response.status_code == 200
    assert len(response.context['companies']) == len(evaluations)
    assert response.context['companies'][0] == companies[0]


# @pytest.mark.django_db
# def test_evaluation_view(client, company):
#     response = client.get(f"/evaluation/{company.pk}")
#
#     assert response.status_code == 200
#     assert response.context['company'] == company

@pytest.mark.django_db
def test_registration_view(client):
    data = {
        'first_name': 'test_name',
        'last_name': 'test_last_name',
        'email': 'test@email.com',
        'password': 'test_password',
        'password_repeated': 'test_password',
    }
    response = client.post("/register/", data)
    assert response.status_code == 302
    user = User.objects.get(email="test@email.com")
    assert user is not None
    assert user.first_name == 'test_name'
    assert user.last_name == 'test_last_name'
    assert user.email == 'test@email.com'
    assert user.is_authenticated

