import os
import pandas as pd
import requests
from datetime import datetime
from django.core.management import BaseCommand

from final_project.settings import BASE_DIR
from final_project.local_settings import API_KEY
from main_app.models import Exchange, Company, Sector, Price, IncomeStatement, BalanceSheet, CashFlowStatement


def get_tickers(csv_file_path):
    """Get 1000 tickers of companies from a csv file"""
    all_tickers = pd.read_csv(csv_file_path)['Symbol']
    tickers = all_tickers[:1000]
    return tickers


def insert_and_get_exchange(exchange_symbol):
    """Insert information about exchange if it does not exist, and return Exchange object"""
    exchange, _ = Exchange.objects.get_or_create(symbol=exchange_symbol)
    return exchange


def insert_and_get_sector(sector_name, exchange):
    """Insert information about sector if it does not exist, and return Sector object"""
    sector, created = Sector.objects.get_or_create(name=sector_name)
    if created:
        sector.exchanges.add(exchange)
        sector.save()
    return sector


def insert_company_data(ticker):
    """
    Pull company's information from financialmodelingprep.com, segregate it and save to database.
    Check if company's sector and exchange is already in database, if not create new objects.
    """

    url = f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()[0]

    # Get and create Exchange object:
    exchange = insert_and_get_exchange(data['exchangeShortName'])

    # Get and create Sector object:
    sector = insert_and_get_sector(data['sector'], exchange)

    # Create Company object:
    if not Company.objects.filter(symbol=ticker).exists():
        Company.objects.create(
            name=data['companyName'],
            symbol=ticker,
            exchange=exchange,
            country=data['country'],
            sector=sector,
            description=data['description'],
            market_cap=data['mktCap'],
            website=data['website'],
        )


def insert_company_price_data(ticker):
    """
    Pull company's price details from financialmodelingprep.com, and save to database.
    Full price history is saved in json format in a models.JSONField
    """
    start = "2018-01-01"
    end = datetime.today().strftime('%Y-%m-%d')
    company = Company.objects.get(symbol=ticker)

    # URL for historical data:
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?from={start}&to={end}&apikey={API_KEY}"
    response = requests.get(url)
    history = response.json()

    # URL for current_price, change and number of shares:
    url_2 = f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={API_KEY}"
    response = requests.get(url_2)
    data = response.json()[0]

    Price.objects.create(
        company=company,
        current_value=data["price"],
        change_percentage=data["changesPercentage"],
        change=data["change"],
        history=history,
        shares_outstanding=data['sharesOutstanding']
    )


def insert_income_statement_data(ticker):
    """Pull income statement data from financialmodelingprep.com,
    segregate it and save to database."""

    url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?limit=120&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    company = Company.objects.get(symbol=ticker)

    for period_data in data:
        IncomeStatement.objects.create(
            company=company,
            year=period_data['calendarYear'],
            total_revenue=period_data['revenue'],
            cost_of_revenue=period_data['costOfRevenue'],
            gross_profit=period_data['grossProfit'],
            gross_profit_ratio=period_data['grossProfitRatio'],
            research_and_development_expenses=period_data['researchAndDevelopmentExpenses'],
            general_and_administrative_expenses=period_data['generalAndAdministrativeExpenses'],
            selling_and_marketing_expenses=period_data['sellingAndMarketingExpenses'],
            selling_general_and_administrative_expenses=period_data['sellingGeneralAndAdministrativeExpenses'],
            other_expenses=period_data['otherExpenses'],
            operating_expenses=period_data['operatingExpenses'],
            cost_and_expenses=period_data['costAndExpenses'],
            interest_income=period_data['interestIncome'],
            interest_expense=period_data['interestExpense'],
            depreciation_and_amortization=period_data['depreciationAndAmortization'],
            ebitda=period_data['ebitda'],
            ebitda_ratio=period_data['ebitdaratio'],
            operating_income=period_data['operatingIncome'],
            operating_income_ratio=period_data['operatingIncomeRatio'],
            total_other_income_expenses_net=period_data['totalOtherIncomeExpensesNet'],
            income_before_tax=period_data['incomeBeforeTax'],
            income_before_tax_ratio=period_data['incomeBeforeTaxRatio'],
            income_tax_expense=period_data['incomeTaxExpense'],
            net_income=period_data['netIncome'],
            net_income_ratio=period_data['netIncomeRatio'],
        )


def insert_balance_sheet_data(ticker):
    """Pull balance sheet statement data from financialmodelingprep.com,
    segregate it and save to database."""

    url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?limit=120&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    company = Company.objects.get(symbol=ticker)

    for period_data in data:
        BalanceSheet.objects.create(
            company=company,
            year=period_data['calendarYear'],
            cash_and_cash_equivalents=period_data['cashAndCashEquivalents'],
            short_term_investments=period_data['shortTermInvestments'],
            cash_and_short_term_investments=period_data['cashAndShortTermInvestments'],
            net_receivables=period_data['netReceivables'],
            inventory=period_data['inventory'],
            other_current_assets=period_data['otherCurrentAssets'],
            total_current_assets=period_data['totalCurrentAssets'],
            property_plant_equipment_net=period_data['propertyPlantEquipmentNet'],
            goodwill=period_data['goodwill'],
            intangible_assets=period_data['intangibleAssets'],
            goodwill_and_intangible_assets=period_data['goodwillAndIntangibleAssets'],
            long_term_investments=period_data['longTermInvestments'],
            tax_assets=period_data['taxAssets'],
            other_non_current_assets=period_data['otherNonCurrentAssets'],
            total_non_current_assets=period_data['totalNonCurrentAssets'],
            other_assets=period_data['otherAssets'],
            total_assets=period_data['totalAssets'],
            account_payables=period_data['accountPayables'],
            short_term_debt=period_data['shortTermDebt'],
            tax_payables=period_data['taxPayables'],
            deferred_revenue=period_data['deferredRevenue'],
            other_current_liabilities=period_data['otherCurrentLiabilities'],
            total_current_liabilities=period_data['totalCurrentLiabilities'],
            long_term_debt=period_data['longTermDebt'],
            deferred_revenue_non_current=period_data['deferredRevenueNonCurrent'],
            deferred_tax_liabilities_non_current=period_data['deferredTaxLiabilitiesNonCurrent'],
            other_non_current_liabilities=period_data['otherNonCurrentLiabilities'],
            total_non_current_liabilities=period_data['totalNonCurrentLiabilities'],
            other_liabilities=period_data['otherLiabilities'],
            capital_lease_obligations=period_data['capitalLeaseObligations'],
            total_liabilities=period_data['totalLiabilities'],
            preferred_stock=period_data['preferredStock'],
            common_stock=period_data['commonStock'],
            retained_earnings=period_data['retainedEarnings'],
            accumulated_other_comprehensive_income_loss=period_data['accumulatedOtherComprehensiveIncomeLoss'],
            other_total_stockholder_equity=period_data['othertotalStockholdersEquity'],
            total_stock_holder_equity=period_data['totalStockholdersEquity'],
            total_equity=period_data['totalEquity'],
            total_liabilities_and_stock_holder_equity=period_data['totalLiabilitiesAndStockholdersEquity'],
            minority_interest=period_data['minorityInterest'],
            total_liabilities_and_total_equity=period_data['totalLiabilitiesAndTotalEquity'],
            total_investments=period_data['totalInvestments'],
            total_debt=period_data['totalDebt'],
            net_debt=period_data['netDebt'],
        )


def insert_cash_flow_statement_data(ticker):
    """
    Pull cash flow statement data from financialmodelingprep.com,
    segregate it and save to database.
    """
    url = f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?limit=120&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    company = Company.objects.get(symbol=ticker)

    for period_data in data:
        CashFlowStatement.objects.create(
            company=company,
            year=period_data['calendarYear'],
            net_income=period_data['netIncome'],
            depreciation_and_amortization=period_data['depreciationAndAmortization'],
            deferred_income_tax=period_data['deferredIncomeTax'],
            stock_based_compensation=period_data['stockBasedCompensation'],
            change_in_working_capital=period_data['changeInWorkingCapital'],
            accounts_receivables=period_data['accountsReceivables'],
            inventory=period_data['inventory'],
            account_payables=period_data['accountsPayables'],
            other_working_capitals=period_data['otherWorkingCapital'],
            other_non_cash_items=period_data['otherNonCashItems'],
            net_cash_provided_by_operating_activities=period_data['netCashProvidedByOperatingActivities'],
            investments_in_property_plant_and_equipment=period_data['investmentsInPropertyPlantAndEquipment'],
            acquisitions_net=period_data['acquisitionsNet'],
            purchases_of_investments=period_data['purchasesOfInvestments'],
            sales_maturities_of_investments=period_data['salesMaturitiesOfInvestments'],
            other_investing_activities=period_data['otherInvestingActivites'],
            net_cash_used_for_investing_activities=period_data['netCashUsedForInvestingActivites'],
            debt_repayment=period_data['debtRepayment'],
            common_stock_issued=period_data['commonStockRepurchased'],
            common_stock_repurchased=period_data['commonStockIssued'],
            dividends_paid=period_data['dividendsPaid'],
            other_financing_activities=period_data['otherFinancingActivites'],
            net_cash_used_provided_by_financing_activities=period_data['netCashUsedProvidedByFinancingActivities'],
            effect_of_forex_changes_on_cash=period_data['effectOfForexChangesOnCash'],
            net_change_in_cash=period_data['netChangeInCash'],
            cash_at_end_of_period=period_data['cashAtEndOfPeriod'],
            cash_at_beginning_of_period=period_data['cashAtBeginningOfPeriod'],
            operating_cash_flow=period_data['operatingCashFlow'],
            capital_expenditure=period_data['capitalExpenditure'],
            free_cash_flow=period_data['freeCashFlow'],
        )


def insert_all_data():
    """
    Call all the insert functions in a loop for every ticker. Count how many companies were added.

    :return: number of companies added or an error if a csv file with a ticker list, does not exist
    or the path to the file is incorrect.
    """

    companies_inserted = 0
    path = os.path.join(BASE_DIR, 'main_app', 'management', 'commands_data', f'data.csv')
    try:
        # tickers = get_tickers(path)
        for ticker in ['NVDA']:
            insert_company_data(ticker)
            insert_company_price_data(ticker)
            insert_income_statement_data(ticker)
            insert_balance_sheet_data(ticker)
            insert_cash_flow_statement_data(ticker)
            companies_inserted += 1

    except FileNotFoundError:
        print(f"No such file or directory: '{path}'")

    return companies_inserted


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
        print("Please wait, the data is loading...")
        companies_inserted = insert_all_data()
        print(f"{companies_inserted} companies were successfully inserted!")
