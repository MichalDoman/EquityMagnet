import os
from django.core.management import BaseCommand
import pandas as pd
import yfinance as yf
import requests
import django

from final_project.settings import BASE_DIR
from main_app.models import Exchange, Company

EXCHANGES = (
    ('nasdaq', 'National Association of Securities Dealers Automated Quotations'),
    # ('nyse', 'New York Stock Exchange')
)


def insert_exchanges_data():
    """Insert information about stock exchanges to database"""
    for exchange in EXCHANGES:
        Exchange.objects.create(name=exchange[1], symbol=exchange[0])


def get_tickers(csv_file_path):
    """Get all the tickers for a stock market form a csv file"""
    tickers = pd.read_csv(csv_file_path)['Symbol']
    return tickers


def function():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main_app.settings')
    django.setup()
    for exchange in EXCHANGES:
        path = os.path.join(BASE_DIR, 'main_app', 'management', 'commands_data', f'{exchange[0]}.csv')

        try:
            for ticker in get_tickers(path):
                if ticker is None:
                    print(str(ticker))
                    break
                company = yf.Ticker(ticker)
                print(ticker)
                # Save company's data to database
                # return company.history(period="1mo)"


        except FileNotFoundError:
            print(f"No such file or directory: '{path}'")
            continue


def get_financial_statements(ticker):
    url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?limit=120&apikey=566b84b1d223b010c6be47cf0bc0bce2"
    response = requests.get(url)
    return response.json()


# print(pd.DataFrame(get_financial_statements("AAPL")).to_string())


class Command(BaseCommand):
    help = """
        Insert companies' data to app's database.
        Data inserted:
         - income statement with components
         - balance sheet with components
         - cash flow statement with components
         - historical price
         - company's details
    """

    def handle(self, *args, **kwargs):
        function()
        print("Data loaded successfully!")
