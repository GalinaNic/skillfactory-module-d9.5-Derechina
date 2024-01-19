
from django import template

register = template.Library()

sensor_list = ['каждый', 'планеты', 'натуральные', 'вызывать', 'Деловой']


@register.filter()
def censor(value):
    for word in sensor_list:
        value = value.replace(word[1:], '*' * len(word[1:]))
    return value
