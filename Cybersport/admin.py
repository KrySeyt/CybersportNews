from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import New, Category, NewComment, User


class NewAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'text', 'slug', 'date', 'image_url', 'category', 'is_published']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']


class NewCommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'created_at', 'new', 'text')


admin.site.register(User, UserAdmin)
admin.site.register(New, NewAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(NewComment, NewCommentAdmin)
