# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


def get_path(instance, filename):
    return 'image/{0}/{1}'.format(instance.user_name, filename)

class User(models.Model):
    user_name = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    phone = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    image = models.FileField(upload_to=get_path)

    def __str__(self):
        return self.user_name
