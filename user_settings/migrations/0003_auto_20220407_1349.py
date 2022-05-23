# Generated by Django 3.2.9 on 2022-04-07 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_settings', '0002_auto_20220407_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='allow_followers',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='settings',
            name='dark_theme',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='settings',
            name='hide_profile',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='settings',
            name='hide_subscribers',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='settings',
            name='turn_on_email_notifications',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
