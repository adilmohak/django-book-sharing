from django import template

register = template.Library()


@register.simple_tag
def get_first_word(str):
    return str[:200]


@register.simple_tag
def get_remain_word(str):
    return str[200:]
