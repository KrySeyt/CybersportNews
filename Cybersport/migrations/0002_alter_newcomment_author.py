# Generated by Django 4.0.2 on 2022-08-29 22:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Cybersport', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newcomment',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
    ]