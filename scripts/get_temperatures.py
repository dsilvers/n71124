#!/usr/bin/python

import requests
from w1thermsensor import W1ThermSensor

for sensor in W1ThermSensor.get_available_sensors():
    id = sensor.id
    temperature = sensor.get_temperature()
    print "Sensor %s has temperature %.2f" % (id, temperature)
    requests.post(
	"http://n71124.com/temperature",
        data={"id": id, "temperature": temperature}
    )

