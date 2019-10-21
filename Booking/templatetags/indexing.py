from django import template

register = template.Library()

@register.filter
def index(value,i):
    index=int(i)
    return value[index]