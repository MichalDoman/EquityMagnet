from statistics import mean
from main_app.utils.general_utils import style_numeric_data

PROJECTION_RANGE = range(1, 6)  # range(1, 6) gives 5 years of projection


class DiscountedCashFlow:
    """A class that stores all functions and data required, for calculating company's share price.
    !!! All methods have to be called in order, due to data being updated with each one of them !!!"""

    def __init__(self, income_statements, balance_sheets, cash_flow_statements):
        """Set necessary attributes, that are used in DCF.
        Get all necessary data from financial statements and price.
        Create a list of financial statements years as well as future years of projection."""

        self.income_statements = income_statements
        self.balance_sheets = balance_sheets
        self.cash_flow_statements = cash_flow_statements

        # Final evaluation values:
        self.enterprise_value = 0
        self.equity_value = 0

        # years:
        self.past_years = []
        self.all_years = []

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
        self.net_working_capital_changes = []
        self.cash_and_cash_equivalents = 0
        self.total_non_current_liabilities = 0
        self.account_payables = 0

        # Cash flow data:
        self.amortization = []
        self.capital_expenditure = []

        # Initial actions:
        self.get_data()
        self.get_years()

        # Index to display years from current to the end of projection:
        self.dcf_index = self.all_years.index(self.past_years[-1])

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
        """Function called in __init__. Gets all necessary data from financial statements."""

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

        last = self.balance_sheets.last()
        self.cash_and_cash_equivalents = last.cash_and_cash_equivalents
        self.total_non_current_liabilities = last.total_non_current_liabilities
        self.account_payables = last.account_payables

        for statement in self.cash_flow_statements:
            self.amortization.append(statement.depreciation_and_amortization)
            self.capital_expenditure.append(statement.investments_in_property_plant_and_equipment)

    def get_years(self):
        """Function called in __init__. Create a list of all years including years of projection."""

        last_period = self.all_years[-1]
        for i in PROJECTION_RANGE:
            self.all_years.append(last_period + i)

    def get_income_projection_dict(self, user_revenue_rate, user_operating_costs, user_other_operating_costs, user_tax):
        """This function collects and calculates all data required in the projection of company's income statement.

        :param user_revenue_rate - A rate of revenues growth in the projection periods, given by user.
        :param user_operating_costs - An average ratio of operating costs in revenue,
        required to set future operating costs, given by user.
        :param user_other_operating_costs - An average ratio of other operating costs in revenue,
        required to set future other operating costs, given by user.
        :param user_tax - A tax rate given by user.

        :return A dictionary. Its keys are the values that are later styled and displayed.
        Items are lists, containing data in order, that is ready to display."""

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
        for _ in PROJECTION_RANGE:
            index = len(self.operating_incomes)
            future_revenue = self.revenues[index]
            future_operating_costs = self.operating_costs[index]
            self.operating_incomes.append(future_revenue - future_operating_costs)
        style_and_update(projection_dict, "operating_income", self.operating_incomes)

        # Update projection dictionary with 'other_operating_costs' key:
        get_values_from_ratio(self.revenues, self.other_operating_costs, user_other_operating_costs)
        style_and_update(projection_dict, "other_operating_costs", self.other_operating_costs)

        # Update projection dictionary with 'income_before_tax' key:
        for _ in PROJECTION_RANGE:
            index = len(self.incomes_before_tax)
            future_income = self.operating_incomes[index]
            future_operating_cost = self.other_operating_costs[index]
            self.incomes_before_tax.append(future_income + future_operating_cost)
        style_and_update(projection_dict, "income_before_tax", self.incomes_before_tax)

        # Update projection dictionary with 'income_tax_expense' key:
        get_values_from_ratio(self.incomes_before_tax, self.income_tax_expenses, user_tax)
        style_and_update(projection_dict, "income_tax_expense", self.income_tax_expenses)

        # Update projection dictionary with 'net_income' key:
        for _ in PROJECTION_RANGE:
            index = len(self.net_incomes)
            future_income = self.incomes_before_tax[index]
            future_expense = self.income_tax_expenses[index]
            self.net_incomes.append(future_income - future_expense)
        style_and_update(projection_dict, "net_income", self.net_incomes)

        return projection_dict

    def get_turnover_ratios_dict(self):
        """This method returns a dictionary, used for data display in a new table,
        containing turnover ratios. The ratios are calculated in the __init__ method."""

        turnover_ratios_dict = {}

        turnover_ratios_dict.update({"year": self.past_years})
        turnover_ratios_dict.update({"receivables_turnover_ratio": self.receivable_turnover_ratios})
        turnover_ratios_dict.update({"inventory_turnover_ratio": self.inventory_turnover_ratios})
        turnover_ratios_dict.update({"liabilities_turnover_ratio": self.liabilities_turnover_ratios})

        return turnover_ratios_dict

    def get_net_working_capital_dict(self):
        """This method gathers data necessary to calculate net working capital,
        and stores it in a dictionary ready to display"""

        net_working_capital_dict = {}

        # Get last year + future years:
        net_working_capital_dict.update({"year": self.all_years[self.dcf_index:]})

        # Calculate future data:
        start_index = len(self.past_years)
        for revenue in self.revenues[start_index:]:
            self.net_receivables.append(int(revenue / 365 * self.average_turnover_ratios['Average'][0]))
            self.inventory.append(int(revenue / 365 * self.average_turnover_ratios['Average'][1]))
            self.total_liabilities.append(int(revenue / 365 * self.average_turnover_ratios['Average'][2]))

        style_and_update(net_working_capital_dict, "net_receivables", self.net_receivables[self.dcf_index:])
        style_and_update(net_working_capital_dict, "inventory", self.inventory[self.dcf_index:])
        style_and_update(net_working_capital_dict, "future_total_liabilities", self.total_liabilities[self.dcf_index:])

        # Get necessary data to calculate net working capital for all years including the first one (if first one is 2020, calculating change, requires 2019 data):
        net_receivables = self.net_receivables[self.dcf_index - 1:]
        inventory = self.inventory[self.dcf_index - 1:]
        total_liabilities = self.total_liabilities[self.dcf_index - 1:]

        # Calculate future net working capital:
        net_working_capital_list = []
        for index, value in enumerate(net_receivables):
            net_working_capital = value + inventory[index] - total_liabilities[index]
            net_working_capital_list.append(net_working_capital)
        style_and_update(net_working_capital_dict, "net_working_capital", net_working_capital_list[1:])

        # Calculate net working capital change:
        previous_value = None
        for index, value in enumerate(net_working_capital_list):
            if previous_value:
                change_value = round(abs(previous_value - value), 2)
                self.net_working_capital_changes.append(change_value)
            previous_value = value
        style_and_update(net_working_capital_dict, "net_working_capital_change", self.net_working_capital_changes)

        return net_working_capital_dict

    def get_capex_dict(self):
        """This method gathers data necessary to calculate capex,
        and stores it in a dictionary ready to display"""

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

    def get_dcf_dict(self, user_wacc, user_g):
        """This method calculates the core of the Discounted Cash Flow evaluation.

        :param user_wacc - a rate o wacc given by user.
        :param user_g - g rate given by user.

        :return A dictionary. It contains all core calculations in a dcf model."""

        dcf_dict = {}

        # Get years:
        dcf_dict.update({"year": self.all_years[self.dcf_index:]})

        # Get periods:
        periods = []
        last_period = len(self.all_years) - self.dcf_index
        for period in range(0, last_period):
            periods.append(period)
        dcf_dict.update({"period": periods})

        # Get revenues and operating costs:
        revenues_list = self.revenues[self.dcf_index:]
        style_and_update(dcf_dict, "revenue", revenues_list)

        operating_costs_list = self.operating_costs[self.dcf_index:]
        style_and_update(dcf_dict, "operating_costs", operating_costs_list)

        # Calculate EBITDA and get amortization:
        amortization_list = self.amortization[self.dcf_index:]
        ebitda_list = []
        for i, value in enumerate(revenues_list):
            ebitda = value - operating_costs_list[i] + amortization_list[i]
            ebitda_list.append(ebitda)
        style_and_update(dcf_dict, "ebitda", ebitda_list)
        style_and_update(dcf_dict, "amortization", amortization_list)

        # Get operating_income and tax expenses:
        operating_income_list = self.operating_incomes[self.dcf_index:]
        style_and_update(dcf_dict, "operating_income", operating_income_list)

        tax_list = self.income_tax_expenses[self.dcf_index:]
        style_and_update(dcf_dict, "income_tax_expenses", tax_list)

        # NOPAT, net working capital changes, amortization, capex
        nopat_list = []
        for i, value in enumerate(operating_income_list):
            nopat = value - tax_list[i]
            nopat_list.append(nopat)
        style_and_update(dcf_dict, "nopat", nopat_list)
        style_and_update(dcf_dict, "amortization_", amortization_list)
        style_and_update(dcf_dict, "net_working_capital_change", self.net_working_capital_changes)
        capex_list = self.capital_expenditure[self.dcf_index:]
        style_and_update(dcf_dict, "capex", capex_list)

        # Calculate residual value:
        residual_value_list = []
        for _ in periods[:-1]:
            residual_value_list.append(0)

        wacc = 0.09
        g = 0.059
        if user_wacc:
            wacc = user_wacc
        if user_g:
            g = user_g
        residual_value = nopat_list[-1] - amortization_list[-1] - self.net_working_capital_changes[-1] - \
                         self.capital_expenditure[-1]
        residual_value *= (1 + g) / (wacc - g)
        residual_value_list.append(int(residual_value))
        style_and_update(dcf_dict, "residual_value", residual_value_list)

        # Calculate Free Cash Flow to Firm:
        fcff_list = []
        for i, value in enumerate(nopat_list):
            fcff = value + amortization_list[i] - self.net_working_capital_changes[i] - capex_list[i] + \
                   residual_value_list[i]
            fcff_list.append(fcff)
        style_and_update(dcf_dict, "free_cash_flow_to_firm", fcff_list)

        # Calculate Discounted Free Cash Flow to Firm:
        dfcff_list = []
        for i, value in enumerate(fcff_list):
            exp = periods[i]
            dfcff = value / (1 + wacc) ** exp
            dfcff_list.append(int(dfcff))
        style_and_update(dcf_dict, "discounted_fcff", dfcff_list)
        self.enterprise_value = sum(dfcff_list)

        return dcf_dict

    def get_share_value_dict(self, current_price, market_cap):
        """Calculate and store in a dictionary, all final results of the dcf calculation.

        :param current_price - company's current stock price.
        :param market_cap - company's market_cap.

        :return A dictionary. It contains all final results of a dcf model."""

        equity_value_dict = {}

        style_and_update(equity_value_dict, "enterprise_value", [self.enterprise_value])
        style_and_update(equity_value_dict, "cash_and_cash_equivalents", [self.cash_and_cash_equivalents])
        debt = self.total_non_current_liabilities + self.account_payables
        style_and_update(equity_value_dict, "debt", [debt])
        self.equity_value = self.enterprise_value + self.cash_and_cash_equivalents - debt
        style_and_update(equity_value_dict, "equity_value", [self.equity_value])

        number_of_shares = int(market_cap / current_price)
        predicted_share_value = round(self.equity_value / number_of_shares, 2)
        equity_value_dict.update({"share_value": [predicted_share_value]})

        return equity_value_dict


def get_average_change(data_list):
    """Calculate an average change in a list of numeric data.
    All changes within consecutive periods are stored in 'changes' list.
    Function returns a mean value of that list."""

    changes = []
    previous_value = None
    for value in data_list:
        if previous_value:
            change = value / previous_value - 1
            changes.append(change)
        previous_value = value

    return mean(changes)


def get_values_from_average_change(values, user_rate=None):
    """Calculate future values for data, basing on its average change.
    Future values are appended to the given list.

    :param values - base values to acquire projection from.
    :param user_rate - None by default. If given by user, average change switches to it."""

    average_change = get_average_change(values)
    if user_rate or user_rate == 0:
        average_change = user_rate

    for _ in PROJECTION_RANGE:
        future_value = values[-1] * (1 + average_change)
        values.append(int(future_value))


def get_average_ratio(nominator_list, denominator_list):
    """ Calculate an average ratio of a value from denominator_list,
    to the corresponding value from nominator_list and get the ratio for every period.

    Parameters are two lists. The ratio is a quotient between denominator list and nominator list.
    """

    ratios = []

    for index in range(1, len(denominator_list)):
        ratio = denominator_list[index] / nominator_list[index]
        ratios.append(round(ratio, 3))

    return mean(ratios)


def get_values_from_ratio(relative_values, key_values, user_ratio=None):
    """Calculate future projection values basing on the current values and their average ratio.
    Results are appended to the key_values list.

    :param relative_values - a list of values within which the ratio of key values is calculated.
    This list contains past and future values already.
    :param key_values - a list of only past values, whose ratio within relative values is calculated.
    This function extends key_values list by the future projection values.
    :param user_ratio - if given it is used as the average ratio of key values in relative values."""

    ratio = get_average_ratio(relative_values, key_values)
    if user_ratio or user_ratio == 0:
        ratio = user_ratio

    for _ in PROJECTION_RANGE:
        index = len(key_values)
        future_revenue = relative_values[index]
        future_costs = future_revenue * ratio
        key_values.append(int(future_costs))


def style_and_update(dictionary, key, items):
    """Using styling functions from general_utils.py,
    style all values from the list and update a given dictionary with them."""

    styled_values = [style_numeric_data(value) for value in items]
    dictionary.update({key: styled_values})


def calculate_turnover_ratio(data, revenues_list):
    """This function is used in __init__ function to calculate turnover ratios for every period.
    The ratios are required to derive an average turnover ratio."""

    ratios = []
    for index, value in enumerate(data):
        ratio = round(value / revenues_list[index] * 365, 2)
        ratios.append(ratio)
    return ratios
