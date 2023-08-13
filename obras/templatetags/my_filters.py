from django import template

register = template.Library()

@register.filter(name='status_to_class')
def status_to_class(status):
    return {
        'EXEC': 'bg-warning',
        'PARA': 'bg-danger',
        'NAO_INI': 'bg-info',
        'CONCL': 'bg-success',
    }.get(status, 'bg-secondary')


@register.filter(name='status_to_border_class')
def status_to_border_class(status):
    return {
        'EXEC': 'border-left-warning',
        'PARA': 'border-left-danger',
        'NAO_INI': 'border-left-info',
        'CONCL': 'border-left-success',
    }.get(status, 'border-left-secondary')


@register.filter(name='status_to_text_class')
def status_to_text_class(status):
    return {
        'EXEC': 'text-warning',
        'PARA': 'text-danger',
        'NAO_INI': 'text-info',
        'CONCL': 'text-success',
    }.get(status, 'text-secondary')


