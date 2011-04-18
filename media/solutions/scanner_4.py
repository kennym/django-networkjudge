import os
import re
import urllib2
from pythonwifi.iwlibs import Wireless

ifid = "wlan0"

wifi = Wireless(ifid)
try:
    networks = wifi.scan()
except RuntimeError:
    print "Must be run as sudo"
    sys.exit()

for network in networks:
    configureSSIDWith(network)
    testConnecitivity()

def configureSSIDWith(network):
    essid = network.essid
    print "Connecting to", essid

    os.system("sudo iwconfig %s essid %s" % (ifid, essid))

    os.system("sudo dhclient %s" % ifid)

def testConnectivity():
    try:
        urllib2.urlopen("http://example.com", timeout=2)
    except urllib2.URLError:
        print "No internet access"
    print "There's internet access"

