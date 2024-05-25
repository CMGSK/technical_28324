from django.db import models
import json


# Create your models here.
class Excel(models.Model):
    file = models.FileField(blank=False, null=False)


