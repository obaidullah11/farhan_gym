# Generated by Django 3.2.10 on 2024-09-15 16:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_delete_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='full_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, default=django.utils.timezone.now, max_length=150, verbose_name='first name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, default=django.utils.timezone.now, max_length=150, verbose_name='last name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('client', 'client'), ('super_admin', 'Super Admin')], default='client', max_length=255),
        ),
    ]
