# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Lfile(models.Model):
    vx = models.CharField(max_length=-1, blank=True, null=True)
    vy = models.CharField(max_length=-1, blank=True, null=True)
    vz = models.CharField(max_length=-1, blank=True, null=True)
    epoch = models.CharField(max_length=-1, blank=True, null=True)
    sigx = models.CharField(max_length=-1, blank=True, null=True)
    sigy = models.CharField(max_length=-1, blank=True, null=True)
    sigz = models.CharField(max_length=-1, blank=True, null=True)
    sigvx = models.CharField(max_length=-1, blank=True, null=True)
    sigvy = models.CharField(max_length=-1, blank=True, null=True)
    sigvz = models.CharField(max_length=-1, blank=True, null=True)
    note = models.CharField(max_length=-1, blank=True, null=True)
    x = models.CharField(max_length=-1, blank=True, null=True)
    y = models.CharField(max_length=-1, blank=True, null=True)
    z = models.CharField(max_length=-1, blank=True, null=True)
    site = models.CharField(max_length=4, blank=True, null=True)
    status = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lfile'
