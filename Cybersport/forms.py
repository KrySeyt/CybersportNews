from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.translation import gettext as _

from .models import New, Category


CATEGORIES = Category.objects.exclude(name='Неизвестно')
DEFAULT_CATEGORY_NAME: str = 'Другое'


class NewForm(forms.ModelForm):
    class Meta:
        model = New
        fields = ['title', 'text', 'image_url', 'is_published', 'category']
        widgets = {
            'text': forms.Textarea()
        }

    def clean_title(self):
        if slugify(self.cleaned_data['title'], allow_unicode=True) == '':
            raise ValidationError(message=_('Из названия невозможно сформировать slug'), code='invalid')
        return self.cleaned_data['title']
