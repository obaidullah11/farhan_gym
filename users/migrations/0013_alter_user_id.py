# Generated by Django 3.2.15 on 2024-05-15 11:45

from django.db import migrations
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20240514_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=users.models.CustomUserIDField(editable=False, max_length=6, primary_key=True, serialize=False),
        ),
    ]
