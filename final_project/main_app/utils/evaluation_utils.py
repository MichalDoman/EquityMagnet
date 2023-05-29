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
    average_change = get_average_change(revenues) if not user_revenue_rate else user_revenue_rate
    print(average_change)
    for _ in range(1, 6):
        future_revenue = revenues[-1] * (1 + average_change)
        revenues.append(int(future_revenue))
    styled_revenues = [style_numeric_data(revenue) for revenue in revenues]
    projection_dict.update({"total_revenue": styled_revenues})

    # Update projection dictionary with 'operational_costs' key:
    operational_costs_ratio = get_average_ratio(revenues, operational_costs)
    if user_operational_costs:
        operational_costs_ratio = user_operational_costs

    for i in range(1, 6):
        index = len(operational_costs.copy())
        future_revenue = revenues[index]
        print(future_revenue)
        print(operational_costs_ratio)
        future_operational_costs = future_revenue * operational_costs_ratio
        operational_costs.append(int(future_operational_costs))
    styled_operational_costs = [style_numeric_data(cost) for cost in operational_costs]
    projection_dict.update({"operational_costs": styled_operational_costs})

    # Update projection dictionary with 'operational_profit' key:
    for index, value in enumerate(revenues):
        operational_profit = value - operational_costs[index]
        operational_profits.append(operational_profit)
    styled_operational_profits = [style_numeric_data(operational_profit) for operational_profit in operational_profits]
    projection_dict.update({"operational_profits": styled_operational_profits})

    # Update projection dictionary with 'other_operational_costs' key:
    for index, value in enumerate(revenues):
        operational_profit = value - operational_costs[index]
        operational_profits.append(operational_profit)

    # Update projection dictionary with 'gross_profit' key:
    other_operational_costs_ratio = get_average_ratio(operational_profits, other_operational_costs)
    if user_other_operational_costs:
        other_operational_costs_ratio = user_other_operational_costs

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
