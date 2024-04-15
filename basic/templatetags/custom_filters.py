from django import template

register = template.Library()

@register.filter(name='dict_key')
def dict_key(dictionary, key):
    return dictionary.get(key, None)