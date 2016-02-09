import socket
import threading
import netifaces
import time

###########################################################################
###########################################################################

class BeaconSender (threading.Thread):
    def __init__(self, port, key, interface):
        threading.Thread.__init__(self)
        self._port = port
        self._key = key
        self._interface = interface
        self._sendEvent = threading.Event()
        self.quit = False

    ################################################

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        assert(self._interface in netifaces.interfaces())
        bcast_addr = netifaces.ifaddresses(self._interface)[netifaces.AF_INET][0]["broadcast"]

        while not self.quit:
            try:
                sock.sendto(self._key, (bcast_addr, self._port))
                
            except socket.error as exc:
                print "Socket error ... continuing anyway"
                continue
            
            time.sleep(1)
        sock.close()
