# Generated by Django 5.0 on 2024-10-17 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('train', '0033_category_exercise_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='set',
            name='Routine',
        ),
        migrations.RemoveField(
            model_name='session',
            name='routine',
        ),
        migrations.RemoveField(
            model_name='set',
            name='exercise',
        ),
        migrations.DeleteModel(
            name='Routine',
        ),
        migrations.DeleteModel(
            name='Session',
        ),
        migrations.DeleteModel(
            name='Set',
        ),
    ]
