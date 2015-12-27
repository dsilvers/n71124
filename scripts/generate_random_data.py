#!/usr/bin/env python

import requests
import random
import time


while True:

    amps = 2.3
    watts = 350.0
    ambient = random.randint(-4, 20)
    cowling = random.randint(10, 30)

    request = requests.post(
        "http://localhost:9000/sensors/",
        data={"serial": "temp:000007295ad2", "value": ambient}
    )
    print request.text

    request = requests.post(
        "http://localhost:9000/sensors/",
        data={"serial": "temp:0000071e0f83", "value": cowling}
    )
    print request.text

    request = requests.post(
        "http://localhost:9000/sensors/",
        data={"serial": "heater:amps", "value": amps}
    )
    print request.text

    request = requests.post(
        "http://localhost:9000/sensors/",
        data={"serial": "heater:watts", "value": watts}
    )
    print request.text

    time.sleep(59)
