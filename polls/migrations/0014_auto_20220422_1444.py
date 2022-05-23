# Generated by Django 3.2.9 on 2022-04-22 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0013_alter_poll_vote_option'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll_vote',
            name='option',
        ),
        migrations.AddField(
            model_name='poll_vote',
            name='poll_option',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='polls.poll_option'),
        ),
    ]