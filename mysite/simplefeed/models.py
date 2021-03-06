from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Target(models.Model):
    url = models.CharField(max_length = 200)
    CATEGORY = (
        ('MN', 'Manga'),
        ('EM', 'Email'),
        ('UR', 'Url'),
    )
    category = models.CharField(max_length = 2, choices = CATEGORY, default = 'UR')
    content = models.CharField(max_length = 10000, default = "")
    diff = models.CharField(max_length = 10000, default = "")
    owner = models.ForeignKey(User, default = 1)
    epoch = models.DateTimeField(auto_now = True)
    def __str__ (self):
        return self.url

class Hash(models.Model):
    owner = models.ForeignKey(User, default = 1)
    hash = models.CharField(max_length = 10000, default = "")
    
