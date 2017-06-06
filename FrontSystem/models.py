# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    qr = models.FileField(upload_to='statics/documents/project/qr', blank=True, null=True)
    enabled = models.BooleanField(default=True)


class ApplyForm(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(blank=True, null=True, max_length=100)
    sex_choices = (("boy","Boy"),("girl","Girl"))
    project = models.ForeignKey(Project)
    sex = models.CharField(choices=sex_choices, max_length=16, default="boy")
    portrait = models.FileField(upload_to='statics/documents/portrait', blank=True, null=True)
    enabled = models.BooleanField(default=True)