from django.contrib import admin

from .models import New, Category


class NewAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'text', 'slug', 'date', 'image_url', 'category', 'is_published']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']


admin.site.register(New, NewAdmin)
admin.site.register(Category, CategoryAdmin)
