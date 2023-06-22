from django.core.management import BaseCommand

from main_app.models import Company
from main_app.management.commands.insert_data import insert_company_price_data


def update_price_models():
    """Update price models for all companies in database."""
    companies = Company.objects.all()
    for company in companies:
        ticker = company.symbol
        insert_company_price_data(ticker, "update")


class Command(BaseCommand):
    help = """Update price models for all companies in database."""

    def handle(self, *args, **kwargs):
        print("Please wait, the data is loading...")
        update_price_models()
        print("Prices have been updated successfully!")
