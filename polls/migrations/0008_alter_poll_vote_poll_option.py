# Generated by Django 3.2.9 on 2022-04-21 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_rename_poll_voter_poll_vote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll_vote',
            name='poll_option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='polls.poll_option'),
        ),
    ]
