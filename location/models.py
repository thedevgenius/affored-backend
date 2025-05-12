from django.db import models
from directory.choices import STATE_CHOICES
from core.utils import generate_unique_slug
# import pygeohash as pgh

# Create your models here.
class Location(models.Model):
    PRECISION_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
    )
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=5, choices=STATE_CHOICES)
    lat = models.FloatField()
    long = models.FloatField()
    precision = models.IntegerField(choices=PRECISION_CHOICES, default=6)
    geohash = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     if not self.geohash:
    #         self.geohash = pgh.encode(self.lat, self.long, precision=self.precision)
    #     return super().save(*args, **kwargs)