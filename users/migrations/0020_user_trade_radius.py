# Generated by Django 3.2.10 on 2024-09-15 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_auto_20240915_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='Trade_radius',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
