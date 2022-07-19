from django.db import models
from django.contrib.postgres.fields import JSONField
from django.dispatch import receiver
from tagging.fields import TagField

COMPLETED = 'COMPLETED'
NOT_COMPLETED = 'NOT_COMPLETED'
STATUS_CHOICES = [
    (COMPLETED, 'Completed'),
    (NOT_COMPLETED, 'Not Completed'),
]


class TerritorialCoverage(models.Model):
    COMPLETED = 'COMPLETED'
    NOT_COMPLETED = 'NOT_COMPLETED'
    STATUS_CHOICES = [
        (COMPLETED, 'Completed'),
        (NOT_COMPLETED, 'Not Completed'),
    ]

    name = models.CharField(max_length=60)
    municod = models.CharField(max_length=60, blank=True)
    aditional_data = models.JSONField(blank=True, null=True)
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=NOT_COMPLETED,
    )

    def __str__(self):
        return self.name

    class Meta:
        permissions = ()


class TerritorialUnit(models.Model):
    ACTIVE = 'ACTIVE'
    NOT_ACTIVE = 'NOT_ACTIVE'
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (NOT_ACTIVE, 'Not Active'),
    ]

    name = models.CharField(max_length=60, blank=True)
    tucode = models.CharField(max_length=60, blank=True)
    geometry = models.JSONField(blank=True, null=True)
    properties = models.JSONField(blank=True, null=True)
    territorial_coverage = models.ForeignKey(
        TerritorialCoverage, on_delete=models.CASCADE, related_name='units')
    tags = TagField()
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=ACTIVE,
    )

    def __str__(self):
        return self.name

    class Meta:
        permissions = ()


class TerritorialUnitImage(models.Model):
    name = models.CharField(max_length=60, blank=True)
    image = models.FileField(blank=True, null=True)
    image_url = models.CharField(max_length=256, blank=True)
    geometry = models.JSONField(blank=True, null=True)
    territorial_unit = models.ForeignKey(
        TerritorialUnit, on_delete=models.CASCADE, related_name='images', default=None)

    def __str__(self):
        return self.name

    class Meta:
        permissions = ()
