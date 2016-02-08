#!/usr/bin/python

import time
import beacon_sender

b = beacon_sender.BeaconSender(12000, b"abc", 'test')
b.daemon = True
b.start()
time.sleep(10000)
