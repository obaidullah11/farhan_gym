# Generated by Django 3.1.7 on 2021-03-08 14:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('train', '0005_auto_20210308_1443'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='datetime',
        ),
        migrations.AddField(
            model_name='session',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]