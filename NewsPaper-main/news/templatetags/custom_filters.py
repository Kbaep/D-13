from django import template

register = template.Library()  # если мы не зарегистрируем наши фильтры, то Django никогда не узнает, где именно их искать и фильтры потеряются

censor_list = ['плохое_слово1', 'плохое_слово2', 'плохое_слово3']

@register.filter(name='censor')
def censor(value):
    for word in censor_list:
        value = value.replace(word, 'censored')
    return value
