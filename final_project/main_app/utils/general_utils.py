from main_app.models import Company, IncomeStatement, BalanceSheet, CashFlowStatement
from main_app.templatetags.templatetags import style_numeric_data


def get_field_dictionaries(queryset):
    """Convert a queryset of FinancialStatement objects into a dictionary.
    Used for displaying data in template while keeping the table heads in the first column.

    :param queryset: A queryset of objects from any of the FinancialStatement models.
    :return: A dictionary where keys are styled, field names of a given FinancialStatement model,
    and the values are lists of field values, for every data year.
    """
    field_names = [field.name for field in queryset[0]._meta.get_fields()]
    field_dictionaries = []

    for field_name in field_names[2:]:  # Exclude company field
        values = []

        # Get all the values for a given field:
        for instance in queryset:
            value = getattr(instance, field_name)
            values.append(value)
        styled_name = field_name.capitalize().replace("_", " ")

        # Apply styles to field's values:
        styled_values = []
        for value in values:
            value = style_numeric_data(value)
            styled_values.append(value
                                 )
        if field_name == "year":  # Do not style 'year' values
            styled_values = values

        field_dictionaries.append({styled_name: styled_values})
    return field_dictionaries


def extract_historical_prices(historical_price_list):
    """Get dates and historical prices from JSON.field of a Price instance,
    and return them in separate lists."""

    dates = []
    close_prices = []
    for daily_price_dict in historical_price_list[::-1]:
        dates.append(daily_price_dict["date"])
        close_prices.append(daily_price_dict["close"])

    return dates, close_prices


def get_all_countries():
    country_set = set()
    for company in Company.objects.all():
        country_set.add(company.country)
    return list(country_set)
