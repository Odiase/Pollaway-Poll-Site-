# Generated by Django 3.2.9 on 2022-04-13 23:07

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20220413_2322'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll_option',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=100, size=[320, 280], upload_to='poll_option_images'),
        ),
    ]
