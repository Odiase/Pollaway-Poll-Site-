# Generated by Django 3.2.9 on 2022-04-13 22:22

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20220413_2318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='expire',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='poll',
            name='image1',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='jpeg', keep_meta=True, null=True, quality=100, size=[320, 280], upload_to='poll_images'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='image2',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='jpeg', keep_meta=True, null=True, quality=100, size=[320, 280], upload_to='poll_images'),
        ),
    ]