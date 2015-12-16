from django.db import models



class Hangar(models.Model):
    name = models.CharField(max_length=60)
    api_key = models.CharField(max_length=120)

    def __unicode__(self):
        return self.name


class Sensor(models.Model):
    name = models.CharField(max_length=60)
    hangar = models.ForeignKey("hangar.Hangar")
    serial = models.CharField(max_length=60, unique=True)
    last_update = models.DateTimeField(blank=True, null=True)
    last_value = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, blank=True)
    unit = models.CharField(max_length=30, blank=True)

    def __unicode__(self):
        return "%s - %s" % (self.hangar, self.name)


class SensorData(models.Model):
    value = models.DecimalField(max_digits=5, decimal_places=2)
    sensor = models.ForeignKey("hangar.Sensor")
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s - %s%s - %s" % ( self.sensor.name, self.value, self.sensor.unit, self.date)


class PowerSchedule(models.Model):
    switch = models.ForeignKey("hangar.PowerSwitch")
    start = models.DateTimeField()
    end = models.DateTimeField()
    departure = models.DateTimeField(blank=True, null=True)

    def __unicode(self):
        return "%s - %s to %s" % (self.switch, self.start, self.end)

class PowerManualControl(models.Model):
    switch = models.ForeignKey("hangar.PowerSwitch")
    date = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()
    status = models.BooleanField()

    def __unicode__(self):
        if self.status:
            status = "ON"
        else:
            status = "OFF"
        return "%s - %s" % (self.switch, status)


class PowerSwitch(models.Model):
    hangar = models.ForeignKey("hangar.Hangar")
    serial = models.CharField(max_length=60, unique=True)

    def __unicode__(self):
        return "%s - %s" % (self.hangar, self.serial)

    def status(self):
        manual_control = PowerManualControl.objects.order_by("-date").first()
        scheduled_control = PowerSchedule.objects.filter(start__gte=datetime.now(), end__lt=datetime.now()).first()

        if scheduled_control:
            if manual_control and not manual_control.status:
                # schedule says turn on, manual control says off
                return False
            else:
                # scheduled to turn on
                return True
        elif manual_control and manual_control.status:
            # manual control says to turn on
            return True
        else:
            return False


