# Generated by Django 3.1.5 on 2021-03-26 08:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gamit', '0015_statistic'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistic',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
