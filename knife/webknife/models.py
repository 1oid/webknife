# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class UserModels(models.Model):
    UserName = models.CharField(max_length=50)
    UserPass = models.CharField(max_length=50)
    CreateDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.UserName

# Create your models here.
class MyShellModels(models.Model):
    user = models.ForeignKey(UserModels)
    target = models.CharField(max_length=200)
    password = models.CharField(max_length=50)
    mark = models.CharField(max_length=50, blank=True, default="无说明")
    ip = models.CharField(max_length=30)
    script = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now_add=True)

