# Generated by Django 3.2.9 on 2022-04-07 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_alter_notification_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='time',
            field=models.DateField(auto_now=True),
        ),
    ]
