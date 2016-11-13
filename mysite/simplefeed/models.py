from __future__ import unicode_literals
from django.db import models

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
    def __str__ (self):
        return self.target_url


