# Generated by Django 3.1.5 on 2021-02-01 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='userip',
            field=models.GenericIPAddressField(null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='asuult',
            field=models.TextField(max_length=1000),
        ),
    ]
