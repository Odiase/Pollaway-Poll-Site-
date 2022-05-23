# Generated by Django 3.2.9 on 2022-04-22 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_auto_20220422_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll_vote',
            name='option',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vote_option', to='polls.poll_option'),
        ),
    ]
