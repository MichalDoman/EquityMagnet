import os
from django.core.management import BaseCommand
import pandas as pd
import yfinance as yf
import requests

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
    tickers[2700] = "NA"  # Symbol NA was switched to NaN value
    return tickers


def yahoo_finance():
    for exchange in EXCHANGES:
        path = os.path.join(BASE_DIR, 'main_app', 'management', 'commands_data', f'{exchange[0]}.csv')

        try:
            tickers = get_tickers(path)
            for ticker in tickers:
                company = yf.Ticker(ticker)
                print(company.info['underlyingSymbol'])

                # return company.history(period="1mo)"

        except FileNotFoundError:
            print(f"No such file or directory: '{path}'")
            continue


def get_income_statements(ticker):
    url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?limit=120&apikey=566b84b1d223b010c6be47cf0bc0bce2"
    response = requests.get(url)
    return response.json()


def get_balance_sheet(ticker):
    url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?limit=120&apikey=566b84b1d223b010c6be47cf0bc0bce2"
    response = requests.get(url)
    return response.json()


def get_cash_flow_statement(ticker):
    url = f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?limit=120&apikey=566b84b1d223b010c6be47cf0bc0bce2"
    response = requests.get(url)
    return response.json()


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
        print(pd.DataFrame(get_cash_flow_statement("AAPL")).to_string())
        print("Data loaded successfully!")
