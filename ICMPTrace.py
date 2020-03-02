from scapy.all import *
import socket

class ICMPTrace:
    probeDetails = {}

    def __init__(self, maxTTL):
        self.maxTTL = maxTTL

    def get_hostname(self, ip):
        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return None


    def probe(self, target):
        target_ip = socket.gethostbyname(target)

        for i in range(1, self.maxTTL):
            pkt = IP(dst=target, ttl=i) / ICMP()
            reply = sr1(pkt, verbose=0)

            if reply is None:
                break
            elif reply.src == target_ip:
                return True
            else:
                self.probeDetails[reply.src] = None

        return False

    def probe_length(self):
        return len(self.probeDetails)

    def show_traceroute(self, target):
        for i in range(1, self.maxTTL):
            pkt = IP(dst=target, ttl=i) / ICMP()
            reply = sr1(pkt, verbose=0)
            print(i,'\t\t',reply.src, '\t\t', self.get_hostname(reply.src))