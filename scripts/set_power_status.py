#!/usr/bin/python

import requests
import time
import RPi.GPIO as io

power_pin = 23

io.setmode(io.BCM)
io.setup(power_pin, io.OUT)
io.output(power_pin, False)

id = "heater"
request = requests.post(
        "http://localhost:9000/switches/",
        data={"serial": id}
)
print request.text



if request.text == "ON":
    io.output(power_pin, True)
else:
    io.output(power_pin, False)
