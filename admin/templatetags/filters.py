from django import template

from babel.dates import format_date
register = template.Library()


@register.filter(name='add_class')
def add_class(value, arg):
    '''
    Add provided classes to form field
    :param value: form field
    :param arg: string of classes seperated by ' '
    :return: edited field
    '''
    css_classes = value.field.widget.attrs.get('class', '')
    # check if class is set or empty and split its content to list (or init list)
    if css_classes:
        css_classes = css_classes.split(' ')
    else:
        css_classes = []
    # prepare new classes to list
    args = arg.split(' ')
    for a in args:
        if a not in css_classes:
            css_classes.append(a)
    # join back to single string
    return value.as_widget(attrs={'class': ' '.join(css_classes)})


@register.filter()
def to_int(value):
    return int(' '.join([char for char in value if char.isdigit()]))+1


@register.filter(name='ru_strftime')
def ru_strftime(value, arg):
    formating_date = format_date(value, arg, locale='ru_RU')
    return str(formating_date)
