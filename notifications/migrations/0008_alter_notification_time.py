# Generated by Django 3.2.9 on 2022-04-07 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0007_alter_notification_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
