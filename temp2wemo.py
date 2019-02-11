"""
temp2dash: Temperatures to Dashing
"""

# pylint: disable=invalid-name

import datetime
import json
import os
import sys
import time
import traceback

import requests

from ouimeaux.environment import Environment
from temperusb import TemperHandler

SCALE = float(os.environ['TEMP_SCALE'])
OFFSET = float(os.environ['TEMP_OFFSET'])
SENSOR = int(os.environ['TEMP_SENSOR'])
SLEEP = int(os.environ['SLEEP_TIME'])
MONITOR_UUID = str(os.environ['MONITOR_UUID'])
MONITOR_URL = "https://hc-ping.com/%s" % MONITOR_UUID


def get_temper():
    th = TemperHandler()
    devs = th.get_devices()
    if len(devs) != 1:
        print "Expected exactly one TEMPer device, found %d" % len(devs)
        sys.exit(1)
    dev = devs[0]

    dev.set_calibration_data(scale=SCALE, offset=OFFSET)

    return dev

temper = get_temper()

wemo = Environment(with_cache=False)
wemo.start()
wemo.discover(seconds=10)
power = wemo.get_switch('freezer')

action = ""
exceptions = 0
exceptions_time = 0
ping_sent = False
while True:
    try:
        temperature = temper.get_temperature(sensor=SENSOR)
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
        if (datetime.datetime.now().time().minute % 10) == 0:
            if not ping_sent:
                requests.post(MONITOR_URL if temperature < -8 else "%s/fail" % MONITOR_URL,
                    data="temperature=%0.1f; switch_state=%s" % (
                        temperature,
                        "on" if power.get_state() == 1 else "off",
                    )
                )
                ping_sent = True
        else:
            ping_sent = False

    except Exception, err:  # pylint: disable=broad-except
        print "\nException on getting temperature\n"
        print traceback.format_exc()
        exceptions += 1
        exceptions_time = time.time()

        # try and reinit temper
        temper = get_temper()

    finally:
        if exceptions > 10:
            requests.post("%s/fail" % MONITOR_URL,
                data="Too many exceptions, exiting"
            )
            print "Too many exceptions, exiting"
            exit(127)
        elif exceptions > 0 and (time.time() - exceptions_time) > (30 * 60):
            # exceptions are non-zero, but less than the threshold for exiting, AND
            # there's been more than 30 minutes elapsed since the first exception: clear the counter
            exceptions = 0

        time.sleep(SLEEP)
