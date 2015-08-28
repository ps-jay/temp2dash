import json
import requests
import sys
from temperusb import TemperHandler


URL="http://dashing:3030/widgets/inside"
SCALE=1.0
OFFSET=-3.0


th = TemperHandler()
devs = th.get_devices()
if len(devs) != 1:
    print "Expected exactly one TEMPer device, found %d" % len(devs)
    sys.exit(1)
dev = devs[0]

dev.set_calibration_data(scale=SCALE, offset=OFFSET)
temperature = dev.get_temperature(sensor=1)

payload = {
    'auth_token': 'abcdefghijklmnopqrstuvwxyz',
    'temperature': '%0.0f%s' % (
        temperature,
        u'\N{DEGREE SIGN}',
    ),
}

post = requests.post(URL, data=json.dumps(payload))

if post.status_code != 204:
    sys.exit(255)

sys.exit(0)
