from django.db import models
from django.contrib.postgres.fields import JSONField
# from django.contrib.auth.models import User
# from django.dispatch import receiver
# from django.db.models.signals import post_save, pre_save
# from tagging.fields import TagField

COMPLETED = 'COMPLETED'
NOT_COMPLETED = 'NOT_COMPLETED'
STATUS_CHOICES = [
    (COMPLETED, 'Completed'),
    (NOT_COMPLETED, 'Not Completed'),
]

class Configuration(models.Model):
    key = models.CharField(max_length=60, blank=False, unique=True, null=False)
    value = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.key
    
    class Meta:
        permissions = ()


class Translation(models.Model):
    language = models.CharField(max_length=256, blank=False, null=False)
    language_code = models.CharField(max_length=256, blank=False, null=False)
    translations = models.JSONField(blank=True, null=True)
