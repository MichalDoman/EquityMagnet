from django.db import models


class Exchange(models.Model):
    name = models.CharField(max_length=255, null=True)
    symbol = models.CharField(max_length=10, unique=True)


class Sector(models.Model):
    name = models.CharField(max_length=255)
    exchanges = models.ManyToManyField(Exchange)


class Company(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    country = models.CharField(max_length=255, null=True)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, null=True)
    description = models.TextField(null=True)
    market_cap = models.BigIntegerField()
    website = models.URLField(null=True)


class Price(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    current_value = models.FloatField()
    history = models.JSONField()


class FinancialStatement(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    year = models.IntegerField()

    class Meta:
        abstract = True


class IncomeStatement(FinancialStatement):
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
