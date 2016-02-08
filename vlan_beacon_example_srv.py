#!/usr/bin/python

import time
import vlan_beacon

b = vlan_beacon.VlanBeacon(12000)
b.daemon = True
b.start()

time.sleep(10000)
