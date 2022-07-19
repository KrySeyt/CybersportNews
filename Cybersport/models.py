import django.utils.timezone
from django.db import models

from django.shortcuts import reverse
from django.template.defaultfilters import slugify


class Category(models.Model):
    class Meta:
        db_table = 'category'
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'

    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Category(name='{self.name}')"


class New(models.Model):
    class Meta:
        db_table = 'new'
        ordering = ['-date']

    title = models.CharField(max_length=300, verbose_name='Заголовок')
    text = models.CharField(max_length=5000, verbose_name='Содержание')
    slug = models.CharField(max_length=300)
    date = models.DateTimeField(default=django.utils.timezone.now)
    image_url = models.CharField(max_length=300, blank=True, verbose_name='Ссылка на изображение')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    is_published = models.BooleanField(verbose_name='Опубликовано')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.title)
        super(New, self).save(force_insert, force_update, using, update_fields)

    def __repr__(self):
        return f"New(title='{self.title}')"

    def get_absolute_url(self):
        return reverse('show-post', self.slug)
