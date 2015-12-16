from __future__ import division
import spidev
import time
import sys
import requests

ZERO_BIAS = 501 # The "zero" value that's read when no power is being run through the sensor
MAX_AMPS = 16.1 # Calculated by the resistor and some magic maths
WIRE_WRAPPED_TIMES = 2 # How many times is the wire wrapped around the sensor?

READINGS_UNTIL_SEND = 1000

def bye():
    global CONN
    if CONN:
        CONN.close()
    sys.exit(0)

def bitstring(n):
    s = bin(n)[2:]
    return '0'*(8-len(s)) + s

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop(0)

    def size(self):
        return len(self.items)

    def avg(self):
        tot = 0
        for it in self.items:
            tot = tot + it
        if self.size() == 0:
            return 0
        return int(tot / self.size())

def connect():
    spi_channel = 0
    CONN = spidev.SpiDev(0, spi_channel)
    CONN.max_speed_hz = 90000 # 1.2 MHz
    return CONN


def read(CONN):
    adc_channel = 0
    cmd = 128
    if adc_channel:
        cmd += 32
    reply_bytes = CONN.xfer2([cmd, 0])
    reply_bitstring = ''.join(bitstring(n) for n in reply_bytes)
    reply = reply_bitstring[5:15]
    return int(reply, 2)

def report(amps, watts):
    request = requests.post(
            "http://n71124.com/sensors/",
            data={"serial": "heater:amps", "value": amps}
    )
    request = requests.post(
            "http://n71124.com/sensors/",
            data={"serial": "heater:watts", "value": watts}
    )
    print "Sent: {} A, {} W".format(amps, watts)
    bye()


CONN = False
READINGS = 0
STACK = Stack()
def show(min, max):
    global STACK, CONN
    global ZERO_BIAS, WIRE_WRAPPED_TIMES, MAX_AMPS
    global READINGS, READINGS_UNTIL_SEND

    val = abs(max - min) * ((1024 - ZERO_BIAS) / MAX_AMPS / WIRE_WRAPPED_TIMES)

    avg = 0
    STACK.push(val)
    if STACK.size() > 25:
        avg = STACK.avg()
        STACK.pop()

    #print "%s,%s,%s mA\t%s W\t%s\t%s" % (min, max, int(val), int(val / 1000 * 120.0), avg, int(avg / 1000 * 120.0))
    READINGS = READINGS + 1
    if READINGS >= READINGS_UNTIL_SEND:
        report(avg, int(avg / 1000 * 120.0))


if __name__ == '__main__':
    MIN_VALUE = 0
    MAX_VALUE = 0
    DIRECTION = 0
    COUNT_SINCE_LAST_SWITCH = 0

    CONN = connect()
    
    try:
        while True:
            val = read(CONN)
            val_biased = val - ZERO_BIAS

            if val == 0 or val == ZERO_BIAS:
                continue

            # Detect switching sides of wave
            # Only record the watts/amps when we've finished coming down from the top of a wave.
            #
            # Direction is positive, but is now negative and below the bias value
            if val_biased <= -1 and DIRECTION == 1 and COUNT_SINCE_LAST_SWITCH > 3:
                if abs(MAX_VALUE - MIN_VALUE) > 4:
                    show(MIN_VALUE, MAX_VALUE)
                MAX_VALUE = val
                COUNT_SINCE_LAST_SWITCH = 0

            # Direction is negative, but value is now positive and above the bias value
            elif val_biased >= 1 and DIRECTION == -1 and COUNT_SINCE_LAST_SWITCH > 3:
                #show(MIN_VALUE, MAX_VALUE)
                MIN_VALUE = val
                COUNT_SINCE_LAST_SWITCH = 0

            # Update max values and direction
            if val_biased >= 0:
                DIRECTION = 1
            else:
                DIRECTION = -1

            if val > MAX_VALUE:
                MAX_VALUE = val
            if val < MIN_VALUE:
                MIN_VALUE = val

            # Doesn't look like we've seen a wave in awhile...
            if COUNT_SINCE_LAST_SWITCH >= 100:
                #print "nothing going on"
                COUNT_SINCE_LAST_SWITCH = 0
                COUNT_SINCE_LAST_SWITCH = COUNT_SINCE_LAST_SWITCH + 1
                READINGS = READINGS + 1
                if READINGS >= READINGS_UNTIL_SEND:
                    report(0, 0)

        # Close SPI connection on quit
    except KeyboardInterrupt:
        bye()
