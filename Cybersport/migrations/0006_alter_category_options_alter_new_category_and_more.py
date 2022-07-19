# Generated by Django 4.0.2 on 2022-07-04 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Cybersport', '0005_category_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterField(
            model_name='new',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Cybersport.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='new',
            name='image_url',
            field=models.CharField(blank=True, max_length=300, verbose_name='Ссылка на изображение'),
        ),
        migrations.AlterField(
            model_name='new',
            name='is_published',
            field=models.BooleanField(verbose_name='Опубликовано'),
        ),
        migrations.AlterField(
            model_name='new',
            name='text',
            field=models.CharField(max_length=5000, verbose_name='Содержание'),
        ),
        migrations.AlterField(
            model_name='new',
            name='title',
            field=models.CharField(max_length=300, verbose_name='Заголовок'),
        ),
    ]