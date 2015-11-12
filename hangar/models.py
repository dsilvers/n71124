from django.db import models

# Create your models here.

class Sensor(models.Model):
    name = models.CharField(max_length=60)
    serial = models.CharField(max_length=60, unique=True)
    last_update = models.DateTimeField(blank=True)
    last_data = models.ForeignKey("hangar.SensorData", related_name="last")

class SensorData(models.Model):
    value = models.DecimalField(max_digits=5, decimal_places=2)
    sensor = models.ForeignKey("hangar.Sensor")
    date = models.DateTimeField(auto_now_add=True)
