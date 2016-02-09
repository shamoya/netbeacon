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
MAX_PKTS = -1

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
        # the method which will be called when a packet is captured
        def _parse_packet(hdr, data):
            print ('%s: captured %d bytes, truncated to %d bytes' % (datetime.datetime.now(), hdr.getlen(), hdr.getcaplen()))
            eth = EthDecoder().decode(data)
            assert(isinstance(eth.child(), ImpactPacket.IP))
            ip = eth.child()
            assert(isinstance(ip.child(), ImpactPacket.UDP))
            udp = ip.child()
            assert(udp.get_uh_dport(), self._port)
            payload = udp.child()
            if payload.get_buffer_as_string() == 'abc':
                print 'received beacon from %s' %  ip.get_ip_src()
                if eth.tag_cnt > 0:
                    print "vlan %d" % eth.get_tag(0).get_vid()

        cap = pcapy.open_live(self._device, SNAPLEN, False, TIMEOUT)
        cap.setfilter('udp port %s' % self._port)
        cap.loop(MAX_PKTS, _parse_packet)
