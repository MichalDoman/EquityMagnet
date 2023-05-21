from main_app.templatetags.style_numeric_data import style_numeric_data


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

# def style_numeric_data(values):
#     """Change style of big integers and percentage data.
#
#     :param values: A list of values to be converted.
#     Big positive or negative integers are displayed in millions and spaced with comas.
#     Float values are changed to percentages with 2 decimal places.
#     :return: A list of styled values.
#     """
#
#     styled_values = []
#     for value in values:
#         if value == 0:
#             pass
#         elif isinstance(value, float):
#             value = str(round((value * 100), 2)) + "%"
#         else:
#             is_negative = False
#             if value < 0:
#                 is_negative = True
#
#             value = str(int(value / 1_000_000))
#             if is_negative:
#                 value = value.strip("-")
#             spaced_value = ""
#             temp_value = ""
#             for digit in value[::-1]:
#                 temp_value += digit
#                 if len(temp_value) % 3 == 0:
#                     spaced_value += temp_value + ","
#                     temp_value = ""
#             spaced_value += temp_value
#             value = spaced_value[::-1].strip(",")
#
#             if is_negative:
#                 value = "-" + value + " M"
#             else:
#                 value += " M"
#         styled_values.append(value)
#     return styled_values
