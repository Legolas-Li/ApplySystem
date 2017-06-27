# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(unique=True, max_length=32)
    nick = models.CharField(max_length=32)
    is_superuser = models.BooleanField(default=False, help_text=u'Super user got more power')

    def __unicode__(self):
        return self.name


def create_profile(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        user.save()
        user_profile = UserProfile(user=user, name=user.username, is_superuser=user.is_superuser)
        user_profile.save()


post_save.connect(create_profile, sender=User)


class Station(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Volunteer(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Active(models.Model):
    name = models.CharField(max_length=100)
    start_at = models.DateTimeField(max_length=100, blank=True, null=True)
    end_at = models.DateTimeField(max_length=100, blank=True, null=True)
    price = models.IntegerField(default=0)
    gift = models.CharField(max_length=100)
    station = models.ManyToManyField(Station)
    volunteer = models.ManyToManyField(Volunteer)
    group = models.ManyToManyField(Group)
    enabled = models.BooleanField(default=True)
    drop_at = models.DateTimeField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return self.name


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
    sex_choices = (("boy","男"),("girl","女"))
    classes = models.ForeignKey(Classes, blank=True, null=True)
    sex = models.CharField(choices=sex_choices, max_length=16, default="boy")
    portrait = models.FileField(upload_to='statics/documents/portrait', blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    enabled = models.BooleanField(default=True)
