import pytest
from django.test import Client
from django.contrib.auth.models import User

from main_app.models import Company, Exchange, FavoriteCompany, Evaluation


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def company():
    exchange = Exchange.objects.create(symbol="EX")
    company = Company.objects.create(
        name="test_company",
        symbol="TEST",
        exchange=exchange,
        country="test_country",
        market_cap=1000000
    )
    return company


@pytest.fixture
def companies():
    exchange = Exchange.objects.create(symbol="EX")
    companies = []
    for i in range(1, 5):
        company = Company.objects.create(
            name=f"company_{i}",
            symbol=f"COM{i}",
            exchange=exchange,
            country=f"country_{i}",
            market_cap=i * 1_000_000
        )
        companies.append(company)
    return companies


@pytest.fixture
def user():
    user = User.objects.create_user(username="test_user", password="test")
    return user


@pytest.fixture
def favorite_companies(user):
    favorite_company = FavoriteCompany.objects.create(
        user=user,
        company=Company.objects.first()
    )
    favorite_company_2 = FavoriteCompany.objects.create(
        user=user,
        company=Company.objects.last()
    )
    return [favorite_company, favorite_company_2]


@pytest.fixture
def evaluations(user):
    evaluation = Evaluation.objects.create(
        user=user,
        company=Company.objects.first(),
        expiration_date="1111-11-11"
    )
    evaluation_2 = Evaluation.objects.create(
        user=user,
        company=Company.objects.last(),
        expiration_date="1111-11-11"
    )
    return [evaluation, evaluation_2]
