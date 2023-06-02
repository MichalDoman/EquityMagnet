from django.db import models
from django.contrib.auth.models import User


class Exchange(models.Model):
    """Exchange markets data"""
    name = models.CharField(max_length=255, null=True)
    symbol = models.CharField(max_length=10, unique=True)


class Sector(models.Model):
    """Companies' sectors names. Every sector can be a part of any exchange market,
    and every exchange can have any sector"""
    name = models.CharField(max_length=255)
    exchanges = models.ManyToManyField(Exchange)


class Company(models.Model):
    """Model representing a company. A company can only be on one exchange market and can be in only one sector."""
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    country = models.CharField(max_length=255, null=True)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, null=True)
    description = models.TextField(null=True)
    market_cap = models.BigIntegerField()
    website = models.URLField(null=True)


class Price(models.Model):
    """Model containing company's current price, its change from the previous period,
    and whole daily history from 2018 dumped in a json field. Every company has only one corresponding Price model.
    This model also keeps number of companies shares.

    All attributes are updated on schedule (except company).
    """

    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    current_value = models.FloatField()
    change_percentage = models.FloatField()
    change = models.FloatField()
    history = models.JSONField()
    shares_outstanding = models.BigIntegerField()


class FinancialStatement(models.Model):
    """A base model for IncomeStatement, BalanceSheet and CashFlowStatement models.
    Each financial statement is assigned to one company and has the same years range.
    Each company can have many financial statement of the same type but for different year."""

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    year = models.IntegerField()

    class Meta:
        abstract = True


class IncomeStatement(FinancialStatement):
    """An expansion of FinancialStatement model containing all income statement's data of a company."""
    total_revenue = models.BigIntegerField()
    cost_of_revenue = models.BigIntegerField()
    gross_profit = models.BigIntegerField()
    gross_profit_ratio = models.FloatField()
    research_and_development_expenses = models.BigIntegerField()
    general_and_administrative_expenses = models.BigIntegerField()
    selling_and_marketing_expenses = models.BigIntegerField()
    selling_general_and_administrative_expenses = models.BigIntegerField()
    other_expenses = models.BigIntegerField()
    operating_expenses = models.BigIntegerField()
    cost_and_expenses = models.BigIntegerField()
    interest_income = models.BigIntegerField(null=True)
    interest_expense = models.BigIntegerField()
    depreciation_and_amortization = models.BigIntegerField()
    ebitda = models.BigIntegerField()
    ebitda_ratio = models.FloatField()
    operating_income = models.BigIntegerField()
    operating_income_ratio = models.FloatField()
    total_other_income_expenses_net = models.BigIntegerField()
    income_before_tax = models.BigIntegerField()
    income_before_tax_ratio = models.FloatField()
    income_tax_expense = models.BigIntegerField()
    net_income = models.BigIntegerField()
    net_income_ratio = models.FloatField()


class BalanceSheet(FinancialStatement):
    """An expansion of FinancialStatement model containing all balance sheet's data of a company."""
    cash_and_cash_equivalents = models.BigIntegerField()
    short_term_investments = models.BigIntegerField()
    cash_and_short_term_investments = models.BigIntegerField()
    net_receivables = models.BigIntegerField()
    inventory = models.BigIntegerField()
    other_current_assets = models.BigIntegerField()
    total_current_assets = models.BigIntegerField()
    property_plant_equipment_net = models.BigIntegerField()
    goodwill = models.BigIntegerField()
    intangible_assets = models.BigIntegerField()
    goodwill_and_intangible_assets = models.BigIntegerField()
    long_term_investments = models.BigIntegerField()
    tax_assets = models.BigIntegerField()
    other_non_current_assets = models.BigIntegerField()
    total_non_current_assets = models.BigIntegerField()
    other_assets = models.BigIntegerField()
    total_assets = models.BigIntegerField()
    account_payables = models.BigIntegerField()
    short_term_debt = models.BigIntegerField()
    tax_payables = models.BigIntegerField()
    deferred_revenue = models.BigIntegerField()
    other_current_liabilities = models.BigIntegerField()
    total_current_liabilities = models.BigIntegerField()
    long_term_debt = models.BigIntegerField()
    deferred_revenue_non_current = models.BigIntegerField()
    deferred_tax_liabilities_non_current = models.BigIntegerField()
    other_non_current_liabilities = models.BigIntegerField()
    total_non_current_liabilities = models.BigIntegerField()
    other_liabilities = models.BigIntegerField()
    capital_lease_obligations = models.BigIntegerField()
    total_liabilities = models.BigIntegerField()
    preferred_stock = models.BigIntegerField()
    common_stock = models.BigIntegerField()
    retained_earnings = models.BigIntegerField()
    accumulated_other_comprehensive_income_loss = models.BigIntegerField()
    other_total_stockholder_equity = models.BigIntegerField()
    total_stock_holder_equity = models.BigIntegerField()
    total_equity = models.BigIntegerField()
    total_liabilities_and_stock_holder_equity = models.BigIntegerField()
    minority_interest = models.BigIntegerField()
    total_liabilities_and_total_equity = models.BigIntegerField()
    total_investments = models.BigIntegerField()
    total_debt = models.BigIntegerField()
    net_debt = models.BigIntegerField()


class CashFlowStatement(FinancialStatement):
    """An expansion of FinancialStatement model containing all cash flow statement's data of a company."""
    net_income = models.BigIntegerField()
    depreciation_and_amortization = models.BigIntegerField()
    deferred_income_tax = models.BigIntegerField()
    stock_based_compensation = models.BigIntegerField()
    change_in_working_capital = models.BigIntegerField()
    accounts_receivables = models.BigIntegerField()
    inventory = models.BigIntegerField()
    account_payables = models.BigIntegerField()
    other_working_capitals = models.BigIntegerField()
    other_non_cash_items = models.BigIntegerField()
    net_cash_provided_by_operating_activities = models.BigIntegerField()
    investments_in_property_plant_and_equipment = models.BigIntegerField()
    acquisitions_net = models.BigIntegerField()
    purchases_of_investments = models.BigIntegerField()
    sales_maturities_of_investments = models.BigIntegerField()
    other_investing_activities = models.BigIntegerField()
    net_cash_used_for_investing_activities = models.BigIntegerField()
    debt_repayment = models.BigIntegerField()
    common_stock_issued = models.BigIntegerField()
    common_stock_repurchased = models.BigIntegerField()
    dividends_paid = models.BigIntegerField()
    other_financing_activities = models.BigIntegerField()
    net_cash_used_provided_by_financing_activities = models.BigIntegerField()
    effect_of_forex_changes_on_cash = models.BigIntegerField()
    net_change_in_cash = models.BigIntegerField()
    cash_at_end_of_period = models.BigIntegerField()
    cash_at_beginning_of_period = models.BigIntegerField()
    operating_cash_flow = models.BigIntegerField()
    capital_expenditure = models.BigIntegerField()
    free_cash_flow = models.BigIntegerField()


class FavoriteCompany(models.Model):
    """A model used for assigning user's favorite companies to the user object.
    One cannot set one company as favorite more than once."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "company")


class Evaluation(models.Model):
    """A model used for assigning users acquired evaluations to the user object.
    Specific company's evaluation is unique and can only be assigned to a user once.

    Purchase date is the date of acquiring the evaluation by the user.
    Expiration date is the date when the user looses their access to the evaluation."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    purchase_date = models.DateField(auto_now_add=True)
    expiration_date = models.DateField()

    class Meta:
        unique_together = ("user", "company")
