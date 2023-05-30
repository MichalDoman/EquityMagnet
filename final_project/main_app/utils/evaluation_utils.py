from main_app.utils.general_utils import style_numeric_data


def get_projection_dict(income_statements, user_revenue_rate, user_operating_costs, user_other_operating_costs, user_tax):
    projection_dict = {}

    years = []
    revenues = []
    operating_costs = []
    operating_incomes = []
    other_operating_costs = []
    incomes_before_tax = []
    income_tax_expenses = []
    net_incomes = []

    # Get necessary data from income statement:
    for statement in income_statements:
        years.append(statement.year)
        revenues.append(statement.total_revenue)
        operating_costs.append(statement.cost_and_expenses)
        operating_incomes.append(statement.operating_income)
        other_operating_costs.append(statement.total_other_income_expenses_net)
        incomes_before_tax.append(statement.income_before_tax)
        income_tax_expenses.append(statement.income_tax_expense)
        net_incomes.append(statement.net_income)

    # Update projection dictionary with 'year' key:
    last_period = years[-1]
    for i in range(1, 6):
        years.append(last_period + i)
    projection_dict.update({"year": years})

    # Update projection dictionary with 'revenue' key:
    average_rate = get_average_change(revenues)
    if user_revenue_rate or user_revenue_rate == 0:
        average_rate = user_revenue_rate

    for _ in range(1, 6):
        future_revenue = revenues[-1] * (1 + average_rate)
        revenues.append(int(future_revenue))
    style_and_update(projection_dict, "total_revenue", revenues)

    # Update projection dictionary with 'operating_costs' key:
    get_costs_from_ratio(revenues, operating_costs, user_operating_costs)
    style_and_update(projection_dict, "operating_costs", operating_costs)

    # Update projection dictionary with 'operating_incomes' key:
    for _ in range(1, 6):
        index = len(operating_incomes)
        future_revenue = revenues[index]
        future_operating_costs = operating_costs[index]
        operating_incomes.append(future_revenue - future_operating_costs)
    style_and_update(projection_dict, "operating_income", operating_incomes)

    # Update projection dictionary with 'other_operating_costs' key:
    get_costs_from_ratio(revenues, other_operating_costs, user_other_operating_costs)
    style_and_update(projection_dict, "other_operating_costs", other_operating_costs)

    # Update projection dictionary with 'income_before_tax' key:
    for _ in range(1, 6):
        index = len(incomes_before_tax)
        future_income = operating_incomes[index]
        future_operating_cost = other_operating_costs[index]
        incomes_before_tax.append(future_income + future_operating_cost)
    style_and_update(projection_dict, "income_before_tax", incomes_before_tax)

    # Update projection dictionary with 'income_tax_expense' key:
    get_costs_from_ratio(incomes_before_tax, income_tax_expenses, user_tax)
    style_and_update(projection_dict, "income_tax_expense", income_tax_expenses)

    # Update projection dictionary with 'net_income' key:
    for _ in range(1, 6):
        index = len(net_incomes)
        future_income = incomes_before_tax[index]
        future_expense = income_tax_expenses[index]
        net_incomes.append(future_income + future_expense)
    style_and_update(projection_dict, "net_income", net_incomes)

    return projection_dict


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
