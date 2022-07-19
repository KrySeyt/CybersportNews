from django import template

from .. import models

OTHER_CATEGORY_NAME: str = 'Другое'
DEFAULT_CATEGORY_NAME: str = 'Неизвестно'


register = template.Library()


@register.simple_tag()
def get_categories():
    categories = models.Category.objects.exclude(name__in=(DEFAULT_CATEGORY_NAME, OTHER_CATEGORY_NAME))
    others_category = models.Category.objects.filter(name=OTHER_CATEGORY_NAME)
    return list(categories) + list(others_category)
