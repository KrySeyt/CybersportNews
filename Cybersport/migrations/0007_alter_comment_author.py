# Generated by Django 4.0.2 on 2022-09-10 11:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Cybersport', '0006_alter_user_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='authors_comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
    ]