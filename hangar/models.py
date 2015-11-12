from django.db import models

# Create your models here.

class Sensor(models.Model):
    name = models.CharField(max_length=60)
    serial = models.CharField(max_length=60, unique=True)
    last_update = models.DateTimeField(blank=True, null=True)
    last_value = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, blank=True)

    def __unicode__(self):
        return self.name

class SensorData(models.Model):
    value = models.DecimalField(max_digits=5, decimal_places=2)
    sensor = models.ForeignKey("hangar.Sensor")
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s - %s - %s" % ( self.sensor.name, self.value, self.date)
