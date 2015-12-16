from django.contrib import admin
from hangar.models import Hangar, Sensor, SensorData, PowerSwitch, PowerSchedule

# Register your models here.

admin.site.register(Hangar)
admin.site.register(Sensor)
admin.site.register(SensorData)
admin.site.register(PowerSwitch)
admin.site.register(PowerSchedule)