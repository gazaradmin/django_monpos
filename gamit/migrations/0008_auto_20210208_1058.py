# Generated by Django 3.1.5 on 2021-02-08 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamit', '0007_auto_20210208_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model_lfile',
            name='sigvx',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='model_lfile',
            name='sigvy',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='model_lfile',
            name='sigvz',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='model_lfile',
            name='sigx',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='model_lfile',
            name='sigy',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='model_lfile',
            name='sigz',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='model_lfile',
            name='vx',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='model_lfile',
            name='vy',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='model_lfile',
            name='vz',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
