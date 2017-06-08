# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Qr(models.Model):
    file =  models.FileField(upload_to='statics/documents/qr', blank=True, null=True)


class Project(models.Model):
    title = models.CharField(max_length=100,blank=True, null=True)
    start_at = models.DateTimeField(max_length=100, blank=True, null=True)
    end_at = models.DateTimeField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)


class Classes(models.Model):
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    # description = models.TextField(blank=True, null=True)
    #qr = models.FileField(upload_to='statics/documents/project/qr', blank=True, null=True)
    qr = models.ForeignKey(Qr, blank=True, null=True)
    enabled = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)


class ApplyForm(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(blank=True, null=True, max_length=100)
    sex_choices = (("boy","Boy"),("girl","Girl"))
    classes = models.ForeignKey(Classes, blank=True, null=True)
    sex = models.CharField(choices=sex_choices, max_length=16, default="boy")
    portrait = models.FileField(upload_to='statics/documents/portrait', blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    enabled = models.BooleanField(default=True)
