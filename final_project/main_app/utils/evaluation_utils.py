from statistics import mean
from main_app.utils.general_utils import style_numeric_data


class DiscountedCashFlow:
    def __init__(self, income_statements, balance_sheets, cash_flow_statements):
        self.income_statements = income_statements
        self.balance_sheets = balance_sheets
        self.cash_flow_statements = cash_flow_statements

        # years:
        self.past_years = []
        self.future_years = []  # years of projection
        self.all_years = []  # past_years & future_years

        # Income statement data:
        self.revenues = []
        self.operating_costs = []
        self.operating_incomes = []
        self.other_operating_costs = []
        self.incomes_before_tax = []
        self.income_tax_expenses = []
        self.net_incomes = []

        # Balance sheet data:
        self.net_receivables = []
        self.inventory = []
        self.total_liabilities = []
        self.total_non_current_assets = []

        # Cash flow data:
        self.amortization = []
        self.capital_expenditure = []

        # Initial actions:
        self.get_data()
        self.get_years()

        # Turnover indexes:
        self.receivable_turnover_ratios = calculate_turnover_ratio(self.net_receivables, self.revenues)
        self.inventory_turnover_ratios = calculate_turnover_ratio(self.inventory, self.revenues)
        self.liabilities_turnover_ratios = calculate_turnover_ratio(self.total_liabilities, self.revenues)
        self.average_turnover_ratios = {"Average": [
            round(mean(self.receivable_turnover_ratios), 2),
            round(mean(self.inventory_turnover_ratios), 2),
            round(mean(self.liabilities_turnover_ratios), 2),
        ]}

    def get_data(self):
        for statement in self.income_statements:
            self.past_years.append(statement.year)
            self.all_years.append(statement.year)
            self.revenues.append(statement.total_revenue)
            self.operating_costs.append(statement.cost_and_expenses)
            self.operating_incomes.append(statement.operating_income)
            self.other_operating_costs.append(statement.total_other_income_expenses_net)
            self.incomes_before_tax.append(statement.income_before_tax)
            self.income_tax_expenses.append(statement.income_tax_expense)
            self.net_incomes.append(statement.net_income)

        for statement in self.balance_sheets:
            self.net_receivables.append(statement.net_receivables)
            self.inventory.append(statement.inventory)
            self.total_liabilities.append(statement.total_liabilities)
            self.total_non_current_assets.append(statement.total_non_current_assets)

        for statement in self.cash_flow_statements:
            self.amortization.append(statement.depreciation_and_amortization)
            self.capital_expenditure.append(statement.investments_in_property_plant_and_equipment)

    def get_years(self):
        last_period = self.all_years[-1]
        for i in range(1, 6):
            self.all_years.append(last_period + i)
            self.future_years.append(last_period + i)

    def get_income_projection_dict(self, user_revenue_rate, user_operating_costs, user_other_operating_costs, user_tax):
        projection_dict = {}

        # Update projection dictionary with 'year' key:
        projection_dict.update({"year": self.all_years})

        # Update projection dictionary with 'revenue' key:
        get_values_from_average_change(self.revenues, user_revenue_rate)
        style_and_update(projection_dict, "total_revenue", self.revenues)

        # Update projection dictionary with 'operating_costs' key:
        get_values_from_ratio(self.revenues, self.operating_costs, user_operating_costs)
        style_and_update(projection_dict, "operating_costs", self.operating_costs)

        # Update projection dictionary with 'operating_incomes' key:
        for _ in range(1, 6):
            index = len(self.operating_incomes)
            future_revenue = self.revenues[index]
            future_operating_costs = self.operating_costs[index]
            self.operating_incomes.append(future_revenue - future_operating_costs)
        style_and_update(projection_dict, "operating_income", self.operating_incomes)

        # Update projection dictionary with 'other_operating_costs' key:
        get_values_from_ratio(self.revenues, self.other_operating_costs, user_other_operating_costs)
        style_and_update(projection_dict, "other_operating_costs", self.other_operating_costs)

        # Update projection dictionary with 'income_before_tax' key:
        for _ in range(1, 6):
            index = len(self.incomes_before_tax)
            future_income = self.operating_incomes[index]
            future_operating_cost = self.other_operating_costs[index]
            self.incomes_before_tax.append(future_income + future_operating_cost)
        style_and_update(projection_dict, "income_before_tax", self.incomes_before_tax)

        # Update projection dictionary with 'income_tax_expense' key:
        get_values_from_ratio(self.incomes_before_tax, self.income_tax_expenses, user_tax)
        style_and_update(projection_dict, "income_tax_expense", self.income_tax_expenses)

        # Update projection dictionary with 'net_income' key:
        for _ in range(1, 6):
            index = len(self.net_incomes)
            future_income = self.incomes_before_tax[index]
            future_expense = self.income_tax_expenses[index]
            self.net_incomes.append(future_income - future_expense)
        style_and_update(projection_dict, "net_income", self.net_incomes)

        return projection_dict

    def get_turnover_ratios_dict(self):
        turnover_ratios_dict = {}

        turnover_ratios_dict.update({"year": self.past_years})
        turnover_ratios_dict.update({"receivables_turnover_ratio": self.receivable_turnover_ratios})
        turnover_ratios_dict.update({"inventory_turnover_ratio": self.inventory_turnover_ratios})
        turnover_ratios_dict.update({"liabilities_turnover_ratio": self.liabilities_turnover_ratios})

        return turnover_ratios_dict

    def get_net_working_capital_dict(self):
        net_working_capital_dict = {}

        # Get last year + future years:
        years_list = self.future_years.copy()
        years_list.insert(0, self.past_years[-1])
        net_working_capital_dict.update({"year": years_list})

        # Calculate future data:
        future_net_receivables = []
        future_inventory = []
        future_total_liabilities = []
        start_index = len(self.past_years) - 1
        for revenue in self.revenues[start_index:-1]:
            future_net_receivables.append(int(revenue / 365 * self.average_turnover_ratios['Average'][0]))
            future_inventory.append(int(revenue / 365 * self.average_turnover_ratios['Average'][1]))
            future_total_liabilities.append(int(revenue / 365 * self.average_turnover_ratios['Average'][2]))

        future_net_receivables.insert(0, self.net_receivables[-1])
        style_and_update(net_working_capital_dict, "net_receivables", future_net_receivables)
        future_inventory.insert(0, self.inventory[-1])
        style_and_update(net_working_capital_dict, "inventory", future_inventory)
        future_total_liabilities.insert(0, self.total_liabilities[-1])
        style_and_update(net_working_capital_dict, "future_total_liabilities", future_total_liabilities)

        # Calculate future net working capital:
        net_working_capital_list = []
        for index, value in enumerate(future_net_receivables):
            net_working_capital = value + future_inventory[index] - future_total_liabilities[index]
            net_working_capital_list.append(net_working_capital)
        style_and_update(net_working_capital_dict, "net_working_capital", net_working_capital_list)

        # Calculate net working capital change:
        nwc_change = ["-"]
        previous_value = None
        for index, value in enumerate(net_working_capital_list):
            if previous_value:
                change_value = round(previous_value - value, 2)
                nwc_change.append(change_value)
            previous_value = value
        style_and_update(net_working_capital_dict, "net_working_capital_change", nwc_change)

        return net_working_capital_dict

    def get_capex_dict(self):
        capex_dict = {}
        capex_dict.update({"year": self.all_years})

        # Calculate non current assets:
        get_values_from_average_change(self.total_non_current_assets)
        style_and_update(capex_dict, "non_current_assets", self.total_non_current_assets)

        # Calculate amortization:
        get_values_from_ratio(self.total_non_current_assets, self.amortization)
        style_and_update(capex_dict, "amortization", self.amortization)

        # Calculate capital expenditure:
        get_values_from_average_change(self.capital_expenditure)
        style_and_update(capex_dict, "capital_expenditure", self.capital_expenditure)

        return capex_dict


def get_average_change(data_list):
    changes = []
    previous_value = None
    for value in data_list:
        if previous_value:
            change = value / previous_value - 1
            changes.append(change)
        previous_value = value

    return mean(changes)


def get_values_from_average_change(values, user_rate=None):
    average_change = get_average_change(values)
    if user_rate or user_rate == 0:
        average_change = user_rate

    for _ in range(1, 6):
        future_value = values[-1] * (1 + average_change)
        values.append(int(future_value))


def get_average_ratio(nominator_list, denominator_list):
    ratios = []

    for index in range(1, len(denominator_list)):
        ratio = denominator_list[index] / nominator_list[index]
        ratios.append(round(ratio, 3))

    return mean(ratios)


def get_values_from_ratio(relative_values, key_values, user_ratio=None):
    ratio = get_average_ratio(relative_values, key_values)
    if user_ratio or user_ratio == 0:
        ratio = user_ratio

    for _ in range(1, 6):
        index = len(key_values)
        future_revenue = relative_values[index]
        future_costs = future_revenue * ratio
        key_values.append(int(future_costs))


def style_and_update(dictionary, key, items):
    styled_values = [style_numeric_data(value) for value in items]
    dictionary.update({key: styled_values})


def calculate_turnover_ratio(data, revenues_list):
    ratios = []
    for index, value in enumerate(data):
        ratio = round(value / revenues_list[index] * 365, 2)
        ratios.append(ratio)
    return ratios
