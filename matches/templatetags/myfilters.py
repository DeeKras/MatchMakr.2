from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})


# TODO: how to make this work?
# @register.filter(name='disable_field')
# def disable_field(value):
#     return value.