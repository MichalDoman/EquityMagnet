import os
from django.core.management import BaseCommand
import pandas as pd
import yfinance as yf
import requests

from final_project.settings import BASE_DIR
from main_app.models import Exchange, Company, Sector, Price, IncomeStatement, BalanceSheet, CashFlowStatement

API_KEY = "566b84b1d223b010c6be47cf0bc0bce2"

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


def insert_income_statement_data(ticker):
    """Pull income statement data from financialmodelingprep.com,
    segregate it and save to database."""

    url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?limit=120&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    company = Company.objects.get(symbol=ticker)

    for _ in data:
        IncomeStatement.objects.create(
            company=company,
            year=data['calendarYear'],
            total_revenue=data['revenue'],
            cost_of_revenue=data['costOfRevenue'],
            gross_profit=data['grossProfit'],
            gross_profit_ratio=data['grossProfitRatio'],
            research_and_development_expenses=data['researchAndDevelopmentExpenses'],
            general_and_administrative_expenses=data['generalAndAdministrativeExpenses'],
            selling_and_marketing_expenses=data['sellingAndMarketingExpenses'],
            selling_general_and_administrative_expenses=data['sellingGeneralAndAdministrativeExpenses'],
            other_expenses=data['otherExpenses'],
            operating_expenses=data['operatingExpenses'],
            cost_and_expenses=data['costAndExpenses'],
            interest_income=data['interestIncome'],
            interest_expense=data['interestExpense'],
            depreciation_and_amortization=data['depreciationAndAmortization'],
            ebitda=['ebitda'],
            ebitda_ratio=data['ebitdaratio'],
            operating_income=data['operatingIncome'],
            operating_income_ratio=data['operatingIncomeRatio'],
            total_other_income_expenses_net=data['totalOtherIncomeExpensesNet'],
            income_before_tax=data['incomeBeforeTax'],
            income_before_tax_ratio=data['incomeBeforeTaxRatio'],
            income_tax_expense=['incomeTaxExpense'],
            net_income=data['netIncome'],
            net_income_ratio=data['netIncomeRatio'],
        )


def get_balance_sheet(ticker):
    """Pull balance sheet statement data from financialmodelingprep.com,
    segregate it and save to database."""

    url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?limit=120&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    company = Company.objects.get(symbol=ticker)

    for _ in data:
        BalanceSheet.objects.create(
            company=company,
            year=data['calendarYear'],
            cash_and_cash_equivalents=data['cashAndCashEquivalents'],
            short_term_investments=data['shortTermInvestments'],
            cash_and_short_term_investments=data['cashAndShortTermInvestments'],
            net_receivables=data['netReceivables'],
            inventory=data['inventory'],
            other_current_assets=data['otherCurrentAssets'],
            total_current_assets=data['totalCurrentAssets'],
            property_plant_equipment_net=data['propertyPlantEquipmentNet'],
            goodwill=data['goodwill'],
            intangible_assets=data['intangibleAssets'],
            goodwill_and_intangible_assets=data['goodwillAndIntangibleAssets'],
            long_term_investments=data['longTermInvestments'],
            tax_assets=data['taxAssets'],
            other_non_current_assets=data['otherNonCurrentAssets'],
            total_non_current_assets=data['totalNonCurrentAssets'],
            other_assets=data['otherAssets'],
            total_assets=data['totalAssets'],
            account_payables=data['accountPayables'],
            short_term_debt=data['shortTermDebt'],
            tax_payables=data['taxPayables'],
            deferred_revenue=data['deferredRevenue'],
            other_current_liabilities=data['otherCurrentLiabilities'],
            total_current_liabilities=data['totalCurrentLiabilities'],
            long_term_debt=data['longTermDebt'],
            deferred_revenue_non_current=data['deferredRevenueNonCurrent'],
            deferred_tax_liabilities_non_current=data['deferredTaxLiabilitiesNonCurrent'],
            other_non_current_liabilities=data['otherNonCurrentLiabilities'],
            total_non_current_liabilities=data['totalNonCurrentLiabilities'],
            other_liabilities=data['otherLiabilities'],
            capital_lease_obligations=data['capitalLeaseObligations'],
            total_liabilities=data['totalLiabilities'],
            preferred_stock=data['preferredStock'],
            common_stock=data['commonStock'],
            retained_earnings=data['retainedEarnings'],
            accumulated_other_comprehensive_income_loss=data['accumulatedOtherComprehensiveIncomeLoss'],
            other_total_stockholder_equity=data['othertotalStockholdersEquity'],
            total_stock_holder_equity=data['totalStockholdersEquity'],
            total_equity=data['totalEquity'],
            total_liabilities_and_stock_holder_equity=data['totalLiabilitiesAndStockholdersEquity'],
            minority_interest=data['minorityInterest'],
            total_liabilities_and_total_equity=data['totalLiabilitiesAndTotalEquity'],
            total_investments=data['totalInvestments'],
            total_debt=data['totalDebt'],
            net_debt=data['netDebt'],
        )


def get_cash_flow_statement(ticker):
    """
    Pull cash flow statement data from financialmodelingprep.com,
    segregate it and save to database.
    """
    url = f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?limit=120&apikey={API_KEY}"
    response = requests.get(url)
    return response.json()


class Command(BaseCommand):
    help = """
        Insert companies' data to app's database.
        Data inserted:
         - income statement with components (5 years)
         - balance sheet with components (5 years)
         - cash flow statement with components (5 years)
         - historical price (since 2000)
         - company's details
    """

    def handle(self, *args, **kwargs):
        # print(pd.DataFrame(insert_income_statement_data("AAPL")).to_string())
        print(insert_income_statement_data("AAPL"))
        print("Data loaded successfully!")
