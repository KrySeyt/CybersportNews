from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import New, Category, NewComment, User, Like, Dislike


@admin.register(New)
class NewAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'text', 'slug', 'date', 'image_url', 'category', 'is_published']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']


@admin.register(NewComment)
class NewCommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'created_at', 'new', 'text')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass


@admin.register(Dislike)
class DislikeAdmin(admin.ModelAdmin):
    pass
