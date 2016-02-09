import pcapy
import threading
import datetime
from impacket.ImpactDecoder import EthDecoder
from impacket import ImpactPacket

###########################################################################
###########################################################################

SNAPLEN = 1024
TIMEOUT = 2000
BEACON_UDP_PORT = 12000
KEY = 'abc'

###########################################################################
###########################################################################

class VlanBeacon(threading.Thread):
    def __init__(self, physical_interface):
        threading.Thread.__init__(self)
        self._key = KEY
        self._port = BEACON_UDP_PORT
        self._device = physical_interface
        self.quit = False

    ################################################

    def run(self):
        cap = pcapy.open_live(self._device, SNAPLEN, False, TIMEOUT)
        cap.setfilter('udp port %s' % self._port)

        while not self.quit:
            try:
                (header, packet) = cap.next()
            except pcapy.PcapError:
                print ('%s: Timeout without a beacon ... continueing anyway' % datetime.datetime.now())
                continue

            print ('%s: captured %d bytes, truncated to %d bytes' % (datetime.datetime.now(), header.getlen(), header.getcaplen()))
            self._parse_packet(packet)

    def _parse_packet(self, packet):
        eth = EthDecoder().decode(packet)
        assert(isinstance(eth.child(), ImpactPacket.IP))
        ip = eth.child()
        assert(isinstance(ip.child(), ImpactPacket.UDP))
        udp = ip.child()
        assert(udp.get_uh_dport(), BEACON_UDP_PORT)
        payload = udp.child()
        print payload.get_buffer_as_string()
        if eth.tag_cnt > 0:
            print "vlan %d" % eth.get_tag(0).get_vid()
