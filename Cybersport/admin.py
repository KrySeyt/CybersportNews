from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import New, Category, Comment, Like, Dislike, User


@admin.register(New)
class NewAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'text', 'slug', 'date', 'image_url', 'category', 'is_published', 'rating', 'comments']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'created_at', 'content_object', 'text')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass


@admin.register(Dislike)
class DislikeAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
