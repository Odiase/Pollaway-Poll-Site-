# Generated by Django 3.2.9 on 2022-05-02 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0016_featured_polls'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll_option',
            name='check',
        ),
    ]
