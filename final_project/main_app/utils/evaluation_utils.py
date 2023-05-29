from main_app.utils.general_utils import style_numeric_data


def get_projection_dict(income_statements, user_revenue_rate, user_operational_costs, user_other_operational_costs):
    projection_dict = {}

    years = []
    revenues = []
    operational_costs = []
    operational_profits = []
    other_operational_costs = []
    gross_profits = []
    net_incomes = []

    # Get necessary data from income statement:
    for statement in income_statements:
        years.append(statement.year)
        revenues.append(statement.total_revenue)
        operational_costs.append(statement.cost_and_expenses)
        other_operational_costs.append(statement.operating_expenses)
        gross_profits.append(statement.gross_profit)
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

    # Update projection dictionary with 'operational_costs' key:
    get_costs_from_ratio(revenues, operational_costs, user_operational_costs)
    style_and_update(projection_dict, "operational_costs", operational_costs)

    # Update projection dictionary with 'operational_profit' key:
    for index, value in enumerate(revenues):
        operational_profit = value - operational_costs[index]
        operational_profits.append(operational_profit)
    style_and_update(projection_dict, "operational_profits", operational_profits)

    # Update projection dictionary with 'other_operational_costs' key:
    get_costs_from_ratio(revenues, other_operational_costs, user_other_operational_costs)
    style_and_update(projection_dict, "other_operational_costs", other_operational_costs)

    # Update projection dictionary with 'gross_profit' key:

    return projection_dict


def style_and_update(dictionary, key, items):
    styled_values = [style_numeric_data(value) for value in items]
    dictionary.update({key: styled_values})


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


def get_costs_from_ratio(revenues, costs, user_ratio):
    ratio = get_average_ratio(revenues, costs)
    if user_ratio or user_ratio == 0:
        ratio = user_ratio

    for _ in range(1, 6):
        index = len(costs)
        future_revenue = revenues[index]
        future_costs = future_revenue * ratio
        costs.append(int(future_costs))
