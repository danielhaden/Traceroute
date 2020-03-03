from scapy.all import *
import socket

class Trace:
    probeDetails = {}
    layer4protocol = None

    def __init__(self, maxTTL):
        self.maxTTL = maxTTL

    def probe_length(self):
        return len(self.probeDetails)

    def get_hostname(self, ip):
        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return None

    def probe(self, target, verbose=False):
        target_ip = socket.gethostbyname(target)

        for i in range(1, self.maxTTL):
            ## set src because scapy will not use current IP when using automated VPN vantage switching
            pkt = IP(dst=target_ip, ttl=i) / self.layer4protocol

            reply = sr1(pkt, verbose=0, timeout=4)

            if reply is None:
                break
            elif reply.src == target_ip:
                if verbose:
                    print("******************************")
                return True
            else:
                ## should add hostname method later
                self.probeDetails[reply.src] = None

                if verbose:
                    if i == 1:
                        print('HOP', '\t', "ROUTER IP", '\t\t\t', "HOSTNAME")

                    print(i, '\t\t', reply.src, '\t\t', self.get_hostname(reply.src))

        if verbose:
            print("***DID NOT REACH TARGET***")

        return False

class ICMPTrace(Trace):
    layer4protocol = ICMP()

class UDPTrace(Trace):
    layer4protocol = UDP()