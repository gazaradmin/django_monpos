# Generated by Django 3.1.5 on 2021-02-04 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamit', '0004_auto_20210204_1119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='user',
        ),
    ]