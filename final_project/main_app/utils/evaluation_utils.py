from main_app.utils.general_utils import style_numeric_data


def get_projection_dict(income_statements, revenue_change, costs_income_ratio):
    projection_dict = {}

    years = []
    revenues = []
    total_costs = []

    # Get necessary data from income statement:
    for statement in income_statements:
        years.append(statement.year)
        revenues.append(statement.total_revenue)
        total_costs.append(statement.cost_and_expenses)

    # Update projection dictionary with 'year' key:
    last_period = years[-1]
    for i in range(1, 6):
        years.append(last_period + i)
    projection_dict.update({"year": years})

    # Update projection dictionary with 'revenue' key:
    average_change = get_average_change(revenues) if not revenue_change else revenue_change
    print(average_change)
    for _ in range(1, 6):
        future_revenue = revenues[-1] * (1 + average_change)
        revenues.append(int(future_revenue))
    styled_revenues = [style_numeric_data(revenue) for revenue in revenues]
    projection_dict.update({"total_revenue": styled_revenues})

    # Update projection dictionary with 'operational_costs' key:
    costs_ratio = get_average_ratio(revenues, total_costs) if not costs_income_ratio else costs_income_ratio
    for i in range(1, 6):
        index = len(total_costs.copy())
        future_revenue = revenues[index]
        print(future_revenue)
        print(costs_ratio)
        future_total_costs = future_revenue * costs_ratio
        total_costs.append(int(future_total_costs))
    styled_total_costs = [style_numeric_data(cost) for cost in total_costs]
    projection_dict.update({"total_costs": styled_total_costs})

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
