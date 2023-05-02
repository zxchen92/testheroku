from django import template

register = template.Library()

@register.filter(name='range_filter')
def range_filter(value, end):
    return range(value, end)
