from django import template

register = template.Library()

@register.filter
def m_date(value):
    try:
        data = value.split('-')
        return data[1]+'.'+data[2]
    except Exception, e:
        return value
