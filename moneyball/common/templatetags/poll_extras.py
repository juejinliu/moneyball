from django import template

register = template.Library()

@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg

@register.filter(name='times')
def times(value, arg):
    return value * arg

@register.filter(name='minus')
def times(value, arg):
    return value - arg