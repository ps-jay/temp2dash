"""
temp2dash: Temperatures to Dashing
"""

# pylint: disable=invalid-name

import json
import os
import sys
import time
import traceback

from ouimeaux.environment import Environment
from temperusb import TemperHandler

SCALE = float(os.environ['TEMP_SCALE'])
OFFSET = float(os.environ['TEMP_OFFSET'])
SENSOR = int(os.environ['TEMP_SENSOR'])
SLEEP = int(os.environ['SLEEP_TIME'])

th = TemperHandler()
devs = th.get_devices()
if len(devs) != 1:
    print "Expected exactly one TEMPer device, found %d" % len(devs)
    sys.exit(1)
dev = devs[0]

dev.set_calibration_data(scale=SCALE, offset=OFFSET)

wemo = Environment(with_cache=False)
wemo.start()
wemo.discover(seconds=10)
power = wemo.get_switch('freezer')

action = ""
exceptions = 0
while True:
    try:
        temperature = dev.get_temperature(sensor=SENSOR)
        state = power.get_state()
        current = "off"
        if state == 1:
            current = "on"

        if temperature > -18:
            action = "temp above -18, turning on"
            if state == 1:
                action = "temp above -18, remaining on"
            power.on()
        elif temperature < -19:
            action = "temp below -19, remaining off"
            if state == 1:
                action = "temp below -19, turning off"
            power.off()
        else:
            action = "temp in range, remaining %s" % current

        print u"%s - %0.1f\u2103C - switch is %s, %s" % (
            time.strftime("%Y-%m-%d %H:%M:%S"),
            temperature,
            current,
            action,
        )

    except Exception, err:  # pylint: disable=broad-except
        print "\nException on getting temperature\n"
        print traceback.format_exc()
        exceptions += 1

    finally:
        if exceptions > 10:
            print "Too many exceptions, exiting"
            exit(127)

        time.sleep(SLEEP)
