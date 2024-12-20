from django.template.defaultfilters import floatformat
from django.template import Library

register = Library()


def formatted_float(value, size):
    """Форматирование точки в числе"""
    value = floatformat(value, arg=size)
    return str(value).replace(',', '.')


register.filter('formatted_float', formatted_float)

