"""
temp2dash: Temperatures to Dashing
"""

# pylint: disable=invalid-name

import json
import os
import time
import traceback

import requests

from envirophat import weather

URL = os.environ['DASHING_URL']
TOKEN = os.environ['DASHING_TOKEN']
SCALE = float(os.environ['TEMP_SCALE'])
OFFSET = float(os.environ['TEMP_OFFSET'])
SLEEP = int(os.environ['SLEEP_TIME'])

reduced_logging = None
while True:
    try:
        temperature = weather.temperature()
    except Exception as err:  # pylint: disable=broad-except
        print("\nException on getting temperature\n")
        print(traceback.format_exc())

    temperature = temperature * SCALE + OFFSET

    payload = {
        'auth_token': TOKEN,
        'temperature': '%0.0f%s' % (
            temperature,
            u'\N{DEGREE SIGN}',
        ),
    }

    if reduced_logging is None or reduced_logging > 900:
        print(u"%s - %0.1f\u2103C" % (
            time.strftime("%Y-%m-%d %H:%M:%S"),
            temperature,
        ))
        reduced_logging = 0

    try:
        post = requests.post(URL, data=json.dumps(payload))
    except Exception as err:  # pylint: disable=broad-except
        print("\nException on posting temperature to dashing\n")
        print(traceback.format_exc())

    if post.status_code != 204:
        print("\nHTTP status from POST was %s (expected 204)\n" % post.status_code)

    time.sleep(SLEEP)
    reduced_logging += SLEEP
