from ICMPTrace import ICMPTrace
from UDPTrace import *
from PIAVPN import PIAVPN
from IP import is_valid_ip

# vpn = PIAVPN()
# vpn.connect_to_region("us-west")


# print(is_valid_ip("125.123.255.255"))
# exit(0)
icmp = UDPTrace(30)

icmp.probe("cu.edu")
print(icmp.probeDetails)
print(icmp.probe_length())


exit(0)

