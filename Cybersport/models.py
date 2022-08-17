import django.utils.timezone
from django.db import models
from django.contrib.auth.models import User

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
        return self.name if self.name != 'Неизвестно' else self.slug

    def __repr__(self):
        return f"Category(name='{self.name}')"


class New(models.Model):
    class Meta:
        db_table = 'new'
        ordering = ['-date']

    title = models.CharField(max_length=300, verbose_name='Заголовок')
    text = models.CharField(max_length=5000, verbose_name='Содержание')
    slug = models.CharField(max_length=300)
    date = models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата')
    image_url = models.CharField(max_length=300, blank=True, verbose_name='Ссылка на изображение')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    is_published = models.BooleanField(verbose_name='Опубликовано')

    def __repr__(self):
        return f"New(title='{self.title}')"

    def get_absolute_url(self):
        return reverse('show-post', self.slug)


class NewComment(models.Model):
    class Meta:
        db_table = 'comment'

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    text = models.CharField(max_length=5000)
    created_at = models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата')
    new = models.ForeignKey(New, on_delete=models.CASCADE)
