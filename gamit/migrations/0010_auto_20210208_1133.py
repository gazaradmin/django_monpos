# Generated by Django 3.1.5 on 2021-02-08 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamit', '0009_auto_20210208_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site_hardware',
            name='Data_Center',
            field=models.CharField(blank=True, default='Monpos', max_length=100, null=True),
        ),
    ]
