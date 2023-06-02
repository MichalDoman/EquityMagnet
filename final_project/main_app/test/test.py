import pytest

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
def test_company_list_filtering_and_sorting(client, companies):
    for sort in SORTING_NAMES:
        response = client.get(f"/companies/?phrase=&exchanges=1&market_cap=&sort_by={sort}")
        assert response.status_code == 200


@pytest.mark.django_db
def test_favorite_company_list_view(client, user, companies, favorite_companies):
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
