# Generated by Django 3.2.10 on 2024-09-11 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_user_latitude_user_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='contact',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
