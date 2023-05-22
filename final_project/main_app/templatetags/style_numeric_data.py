from django import template

register = template.Library()


@register.filter(name="style_numeric_data")
def style_numeric_data(value):
    """Change style of big integers and percentage data.

    :param value: A value to be converted.
    Big positive or negative integers are displayed in millions and spaced with comas.
    Float values are changed to percentages with 2 decimal places.
    :return: A styled value.
    """

    if value == 0:
        pass
    elif isinstance(value, float):
        value = str(round((value * 100), 2)) + "%"
    else:
        is_negative = False
        if value < 0:
            is_negative = True

        value = str(int(value / 1_000_000))
        if is_negative:
            value = value.strip("-")
        spaced_value = ""
        temp_value = ""
        for digit in value[::-1]:
            temp_value += digit
            if len(temp_value) % 3 == 0:
                spaced_value += temp_value + ","
                temp_value = ""
        spaced_value += temp_value
        value = spaced_value[::-1].strip(",")

        if is_negative:
            value = "-" + value

    return value
