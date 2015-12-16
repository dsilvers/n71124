#!/usr/bin/python

import requests
from w1thermsensor import W1ThermSensor

for sensor in W1ThermSensor.get_available_sensors():
    id = sensor.id
    temperature = round(sensor.get_temperature(), 2)
    print "Sensor %s has temperature %s" % (id, temperature)
    request = requests.post(
        "http://n71124.com/sensors/",
        data={"serial": id, "value": temperature}
    )
    print request.text
    print "---"