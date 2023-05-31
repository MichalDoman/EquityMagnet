from main_app.utils.general_utils import style_numeric_data


class DiscountedCashFlow:
    def __init__(self, income_statements, balance_sheets):
        self.income_statements = income_statements
        self.balance_sheets = balance_sheets

        # Income statement data:
        self.years = []
        self.revenues = []
        self.operating_costs = []
        self.operating_incomes = []
        self.other_operating_costs = []
        self.incomes_before_tax = []
        self.income_tax_expenses = []
        self.net_incomes = []

        # Balance sheet data:
        self.net_receivables = []

        # Indexes:
        self.receivable_turnover_ratios = []

        # Initial actions:
        self.get_data()

    def get_data(self):
        for statement in self.income_statements:
            self.years.append(statement.year)
            self.revenues.append(statement.total_revenue)
            self.operating_costs.append(statement.cost_and_expenses)
            self.operating_incomes.append(statement.operating_income)
            self.other_operating_costs.append(statement.total_other_income_expenses_net)
            self.incomes_before_tax.append(statement.income_before_tax)
            self.income_tax_expenses.append(statement.income_tax_expense)
            self.net_incomes.append(statement.net_income)

        for statement in self.balance_sheets:
            self.net_receivables.append(statement.net_receivables)

    def get_income_projection_dict(self, user_revenue_rate, user_operating_costs,
                                   user_other_operating_costs,
                                   user_tax):
        projection_dict = {}

        # Update projection dictionary with 'year' key:
        last_period = self.years[-1]
        for i in range(1, 6):
            self.years.append(last_period + i)
        projection_dict.update({"year": self.years})

        # Update projection dictionary with 'revenue' key:
        average_rate = get_average_change(self.revenues)
        if user_revenue_rate or user_revenue_rate == 0:
            average_rate = user_revenue_rate

        for _ in range(1, 6):
            future_revenue = self.revenues[-1] * (1 + average_rate)
            self.revenues.append(int(future_revenue))
        style_and_update(projection_dict, "total_revenue", self.revenues)

        # Update projection dictionary with 'operating_costs' key:
        get_costs_from_ratio(self.revenues, self.operating_costs, user_operating_costs)
        style_and_update(projection_dict, "operating_costs", self.operating_costs)

        # Update projection dictionary with 'operating_incomes' key:
        for _ in range(1, 6):
            index = len(self.operating_incomes)
            future_revenue = self.revenues[index]
            future_operating_costs = self.operating_costs[index]
            self.operating_incomes.append(future_revenue - future_operating_costs)
        style_and_update(projection_dict, "operating_income", self.operating_incomes)

        # Update projection dictionary with 'other_operating_costs' key:
        get_costs_from_ratio(self.revenues, self.other_operating_costs, user_other_operating_costs)
        style_and_update(projection_dict, "other_operating_costs", self.other_operating_costs)

        # Update projection dictionary with 'income_before_tax' key:
        for _ in range(1, 6):
            index = len(self.incomes_before_tax)
            future_income = self.operating_incomes[index]
            future_operating_cost = self.other_operating_costs[index]
            self.incomes_before_tax.append(future_income + future_operating_cost)
        style_and_update(projection_dict, "income_before_tax", self.incomes_before_tax)

        # Update projection dictionary with 'income_tax_expense' key:
        get_costs_from_ratio(self.incomes_before_tax, self.income_tax_expenses, user_tax)
        style_and_update(projection_dict, "income_tax_expense", self.income_tax_expenses)

        # Update projection dictionary with 'net_income' key:
        for _ in range(1, 6):
            index = len(self.net_incomes)
            future_income = self.incomes_before_tax[index]
            future_expense = self.income_tax_expenses[index]
            self.net_incomes.append(future_income + future_expense)
        style_and_update(projection_dict, "net_income", self.net_incomes)

        return projection_dict

    def get_net_working_capital_projection_dict(self):
        projection_dict = {}

    def get_turnover_ratios(self):
        for index, value in enumerate(self.revenues):
            receivables = round(self.net_receivables[index]/value * 365, 2)
            self.receivable_turnover_ratios.append(receivables)



def get_average_change(data_list):
    changes = []
    previous_value = None
    for value in data_list:
        if previous_value:
            change = value / previous_value - 1
            changes.append(change)
        previous_value = value

    return sum(changes) / len(changes)


def get_average_ratio(nominator_list, denominator_list):
    ratios = []

    for index in range(1, len(denominator_list)):
        ratio = denominator_list[index] / nominator_list[index]
        ratios.append(round(ratio, 3))

    return sum(ratios) / len(ratios)


def style_and_update(dictionary, key, items):
    styled_values = [style_numeric_data(value) for value in items]
    dictionary.update({key: styled_values})


def get_costs_from_ratio(revenues, costs, user_ratio):
    ratio = get_average_ratio(revenues, costs)
    if user_ratio or user_ratio == 0:
        ratio = user_ratio

    for _ in range(1, 6):
        index = len(costs)
        future_revenue = revenues[index]
        future_costs = future_revenue * ratio
        costs.append(int(future_costs))
