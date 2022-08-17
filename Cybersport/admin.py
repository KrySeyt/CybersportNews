from django.contrib import admin

from .models import New, Category, NewComment


class NewAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'text', 'slug', 'date', 'image_url', 'category', 'is_published']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']


class NewCommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'created_at', 'new', 'text')


admin.site.register(New, NewAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(NewComment, NewCommentAdmin)
