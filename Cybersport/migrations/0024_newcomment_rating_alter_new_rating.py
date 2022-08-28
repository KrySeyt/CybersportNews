# Generated by Django 4.0.2 on 2022-08-28 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Cybersport', '0023_alter_dislike_rating_alter_dislike_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='newcomment',
            name='rating',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comment', to='Cybersport.rating'),
        ),
        migrations.AlterField(
            model_name='new',
            name='rating',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='new', to='Cybersport.rating'),
        ),
    ]
