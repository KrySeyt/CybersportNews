from functools import singledispatchmethod

import django.utils.timezone
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType

from django.shortcuts import reverse


class CustomUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if 'rating' not in extra_fields:
            extra_fields['rating'] = Rating.objects.create()
        super(CustomUserManager, self).create_user(username=username, email=email, password=password, **extra_fields)


class User(AbstractUser):
    objects = CustomUserManager()

    rating = models.OneToOneField('Rating', on_delete=models.SET_NULL, related_name='custom_user', null=True)
    comments = GenericRelation('Comment')


class LikeManager(models.Manager):
    @singledispatchmethod
    def __contains__(self, like):
        return self.filter(user=like.user, rating=like.rating)

    @__contains__.register
    def _(self, user: User):
        return self.filter(user=user).exists()


class DislikeManager(models.Manager):
    @singledispatchmethod
    def __contains__(self, dislike):
        return self.filter(user=dislike.user, rating=dislike.rating)

    @__contains__.register
    def _(self, user: User):
        return self.filter(user=user).exists()


class Like(models.Model):
    class Meta:
        unique_together = ('user', 'rating')

    objects = LikeManager()

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

    objects = DislikeManager()

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


class NewManager(models.Manager):
    def create(self, *args, **kwargs):
        if 'rating' not in kwargs:
            kwargs['rating'] = Rating.objects.create()
        return super(NewManager, self).create(*args, **kwargs)


class New(models.Model):
    class Meta:
        db_table = 'new'
        ordering = ['-date']

    objects = NewManager()

    title = models.CharField(max_length=300, verbose_name='Заголовок')
    text = models.CharField(max_length=5000, verbose_name='Содержание')
    slug = models.SlugField(max_length=300)
    date = models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата')
    image_url = models.CharField(max_length=300, blank=True, verbose_name='Ссылка на изображение')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    is_published = models.BooleanField(verbose_name='Опубликовано')
    rating = models.OneToOneField(Rating, on_delete=models.SET_NULL, related_name='new', null=True)
    comments = GenericRelation('Comment')

    def __repr__(self):
        return f"New(title='{self.title}')"

    def get_absolute_url(self):
        return reverse('show-post', self.slug)


class NewCommentQuerySet(models.QuerySet):
    def get_likes_count(self):
        return self.aggregate(Count('rating__likes'))['rating__likes__count']

    def get_dislikes_count(self):
        return self.aggregate(Count('rating__dislikes'))['rating__dislikes__count']


class CommentManager(models.Manager):
    def get_queryset(self):
        return NewCommentQuerySet(self.model, using=self._db)

    def create(self, *args, **kwargs):
        if 'rating' not in kwargs:
            kwargs['rating'] = Rating.objects.create()
        return super(CommentManager, self).create(*args, **kwargs)


class Comment(models.Model):
    class Meta:
        db_table = 'comment'

    objects = CommentManager()

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Автор',
                               related_name='comments')
    text = models.CharField(max_length=5000)
    created_at = models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата')
    rating = models.OneToOneField(Rating, on_delete=models.SET_NULL, related_name='related_comment', null=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id',)
