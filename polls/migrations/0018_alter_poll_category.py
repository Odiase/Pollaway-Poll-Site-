# Generated by Django 3.2.9 on 2022-05-05 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0017_remove_poll_option_check'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='category',
            field=models.CharField(choices=[('anime', 'anime'), ('beauty', 'beauty'), ('business & finance', 'business & finance'), ('education', 'education'), ('entertainment', 'entertainment'), ('fashion', 'fashion'), ('food', 'food'), ('government & Politics', 'government & politics'), ('lifestyle', 'lifestyle'), ('movies', 'movies'), ('music', 'music'), ('others', 'others'), ('relationships', 'relationships'), ('religion', 'religion'), ('sports', 'sports'), ('technology', 'technology')], max_length=100),
        ),
    ]