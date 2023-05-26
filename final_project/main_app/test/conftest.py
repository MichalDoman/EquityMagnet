import pytest
from django.test import Client

from main_app.models import Company, Exchange


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def exchange():
    exchange = Exchange.objects.create(symbol="EX")
    return exchange


@pytest.fixture
def companies():
    companies = []
    for i in range(1, 5):
        company = Company.objects.create(
            name=f"company_{i}",
            symbol=f"COM{i}",
            exchange=Exchange.objects.first(),
            market_cap=i
        )
        companies.append(company)
    return companies
