from django import template


register = template.Library()

censor_list = ['politics', 'Politics', 'politic']


# Регистрируем наш фильтр под именем censor, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(value):
    """
    value: значение, к которому нужно применить фильтр
    """
    # Возвращаемое функцией значение подставится в шаблон.
    for word in censor_list:
        value = value.replace(word[1:], '*' * len(word[1:]))
    return value
