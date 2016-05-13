import json
import os
import requests
import sys
import time
import traceback
from temperusb import TemperHandler

URL = os.environ['DASHING_URL']
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

while True:
    try:
	temperature = dev.get_temperature(sensor=SENSOR)
    except Exception, err:
        print "\nException on getting temperature\n"
        print traceback.format_exc()

    payload = {
        'auth_token': 'abcdefghijklmnopqrstuvwxyz',
        'temperature': '%0.0f%s' % (
            temperature,
            u'\N{DEGREE SIGN}',
        ),
    }

    sys.stdout.write(u'%0.1f%s, ' % (
        temperature,
        u'\N{DEGREE SIGN}',
    ))
    sys.stdout.flush()

    try:
        post = requests.post(URL, data=json.dumps(payload))
    except Exception, err:
        print "\nException on posting temperature to dashing\n"
        print traceback.format_exc()

    if post.status_code != 204:
        print "\nHTTP status from POST was %s (expected 204)\n" % post.status_code

    time.sleep(SLEEP)
