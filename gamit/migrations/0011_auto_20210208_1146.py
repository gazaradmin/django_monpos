# Generated by Django 3.1.5 on 2021-02-08 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamit', '0010_auto_20210208_1133'),
    ]

    operations = [
        migrations.RenameField(
            model_name='site_hardware',
            old_name='east',
            new_name='south',
        ),
        migrations.AddField(
            model_name='site_hardware',
            name='Antenna',
            field=models.CharField(max_length=100, null=True),
        ),
    ]