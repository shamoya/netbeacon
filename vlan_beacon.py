import pcapy
import threading
import datetime
from impacket.ImpactDecoder import EthDecoder
from impacket import ImpactPacket

###########################################################################
###########################################################################

DEVICE = 'test'
SNAPLEN = 1024

###########################################################################
###########################################################################

class VlanBeacon(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
        self.quit = False
        devices = pcapy.findalldevs()
        print devices

    ################################################

    def run(self):
        cap = pcapy.open_live(DEVICE, SNAPLEN, True, 0)
        cap.setfilter('udp port %s' % self.port)

        while not self.quit:
            (header, packet) = cap.next()
            print ('%s: captured %d bytes, truncated to %d bytes' %(datetime.datetime.now(), header.getlen(), header.getcaplen()))
            self._parse_packet(packet)

    def _parse_packet(self, packet):
        eth = EthDecoder().decode(packet)
        assert(isinstance(eth.child(), ImpactPacket.IP))
        ip = eth.child()
        assert(isinstance(ip.child(), ImpactPacket.UDP))
        print eth
