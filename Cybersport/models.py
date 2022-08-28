from functools import singledispatchmethod

import django.utils.timezone
from django.db import models
from django.contrib.auth.models import User

from django.shortcuts import reverse


class Like(models.Model):
    class Meta:
        unique_together = ('user', 'rating')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    rating = models.ForeignKey('Rating', on_delete=models.CASCADE, related_name='likes')

    def __init__(self, *args, **kwargs):
        super(Like, self).__init__(*args, **kwargs)
        dislike = self.rating.dislikes.filter(user=self.user)
        if dislike:
            dislike.delete()

    def __repr__(self):
        return f'Like(pk={self.pk}, user={self.user}, object={self.rating.related_object})'


class Dislike(models.Model):
    class Meta:
        unique_together = ('user', 'rating')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dislikes')
    rating = models.ForeignKey('Rating', on_delete=models.CASCADE, related_name='dislikes')

    def __init__(self, *args, **kwargs):
        super(Dislike, self).__init__(*args, **kwargs)
        like = self.rating.likes.filter(user=self.user)
        if like:
            like.delete()

    def __repr__(self):
        return f'Dislike(pk={self.pk}, user={self.user}, object={self.rating.related_object})'


class Rating(models.Model):
    likes = ...
    dislikes = ...

    def is_user_liked(self, user: User) -> bool:
        return self.likes.filter(user=user).exists()

    def is_user_disliked(self, user: User) -> bool:
        return self.dislikes.filter(user=user).exists()

    @singledispatchmethod
    def __contains__(self, item: User | Like | Dislike):
        pass

    @__contains__.register
    def _(self, user: User):
        return self.likes.filter(user=user).union(self.dislikes.filter(user=user)).exists()

    @__contains__.register
    def _(self, like: Like):
        print('LIKE CALLED')
        return like in self.likes

    @__contains__.register
    def _self(self, dislike: Dislike):
        return dislike in self.dislikes


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
    rating = models.OneToOneField(Rating, on_delete=models.SET_NULL, related_name='related_object', null=True)

    def __repr__(self):
        return f"New(title='{self.title}')"

    def get_absolute_url(self):
        return reverse('show-post', self.slug)

    def save(self, *args, **kwargs):
        if not self.rating:
            self.rating = Rating.objects.create()
        super(New, self).save(*args, **kwargs)


class NewComment(models.Model):
    class Meta:
        db_table = 'comment'

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    text = models.CharField(max_length=5000)
    created_at = models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата')
    new = models.ForeignKey(New, on_delete=models.CASCADE)
