# Generated by Django 3.1.7 on 2021-03-11 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('train', '0017_auto_20210311_0101'),
    ]

    operations = [
        migrations.AddField(
            model_name='setgroup',
            name='kaatsu',
            field=models.BooleanField(default=False),
        ),
    ]
