# TP3 : On va router des trucs

## Sommaire
## I. ARP

### 1. Echange ARP

🌞**Générer des requêtes ARP**
````
[quentin@localhost ~]$ ping 10.3.1.12
PING 10.3.1.12 (10.3.1.12) 56(84) bytes of data.
64 bytes from 10.3.1.12: icmp_seq=1 ttl=64 time=0.327 ms
64 bytes from 10.3.1.12: icmp_seq=2 ttl=64 time=0.912 ms
^C
--- 10.3.1.12 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1023ms
rtt min/avg/max/mdev = 0.327/0.619/0.912/0.292 ms
````
````
[quentin@localhost ~]$ ip n s
[...]
10.3.1.12 dev enp0s8 lladdr 08:00:27:99:1a:7b REACHABLE
````
````
[quentin@localhost ~]$ ip link show
2: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 08:00:27:99:1a:7b brd ff:ff:ff:ff:ff:ff
````
### 2. Analyse de trames

🌞**Analyse de trames**

[trames](./dossier_photo/trames_arp3.pcapng)

## II. Routage

### 1. Mise en place du routage

🌞**Activer le routage sur le noeud `router`**
````
[quentin@localhost ~]$ sudo firewall-cmd --list-all
public (active)
  masquerade: yes
````

🌞**Ajouter les routes statiques nécessaires pour que `john` et `marcel` puissent se `ping`**

````
10.3.2.0/24 via 10.3.1.254 dev enp0s8
````
````
[quentin@localhost netw
ork-scripts]$ ping 10.3.2.12
PING 10.3.2.12 (10.3.2.12) 56(84) bytes of data.
64 bytes from 10.3.2.12: icmp_seq=1 ttl=63 time=1.02 ms
64 bytes from 10.3.2.12: icmp_seq=2 ttl=63 time=1.29 ms
64 bytes from 10.3.2.12: icmp_seq=3 ttl=63 time=1.35 ms
^C
--- 10.3.2.12 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2004ms
rtt min/avg/max/mdev = 1.020/1.220/1.349/0.143 ms
````


### 2. Analyse de trames

🌞**Analyse des échanges ARP**

[trames](./dossier_photo/trames_ping_tp3.pcapng)


| ordre | type trame  | IP source | MAC source              | IP destination | MAC destination              |
|-------|-------------|-----------|-------------------------|----------------|------------------------------|
| 1     | Requête ARP | 10.3.2.254| (08:00:27:74:94:58)     | 10.3.2.255     | Broadcast `FF:FF:FF:FF:FF:FF`|
| 2     | Réponse ARP | 10.3.2.12 | (08:00:27:99:1a:7b)     | 10.3.2.254     | (08:00:27:74:94:58)          |
| 3     | Ping        | 10.3.2.254| (08:00:27:74:94:58)     | 10.3.2.12      | (08:00:27:99:1a:7b)          |
| 4     | Pong        | 10.3.2.12 | (08:00:27:99:1a:7b)     | 10.3.2.254     | (08:00:27:74:94:58)          |
| 1     | Requête ARP | 10.3.2.12 | (08:00:27:99:1a:7b)     | 10.3.2.255     | Broadcast `FF:FF:FF:FF:FF:FF`|
| 2     | Réponse ARP | 10.3.2.12 | (08:00:27:99:1a:7b)     | 10.3.2.12      | (08:00:27:99:1a:7b)          |

### 3. Accès internet

🌞**Donnez un accès internet à vos machines**
````
[quentin@localhost ~]$ ping 1.1.1.1
PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.
64 bytes from 1.1.1.1: icmp_seq=1 ttl=55 time=13.3 ms
64 bytes from 1.1.1.1: icmp_seq=2 ttl=55 time=13.8 ms
64 bytes from 1.1.1.1: icmp_seq=3 ttl=55 time=13.0 ms
^C
--- 1.1.1.1 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/mdev = 13.012/13.343/13.757/0.309 ms
````
````
[quentin@localhost etc]$ ping google.com
PING google.com (142.250.74.238) 56(84) bytes of data.
64 bytes from par10s40-in-f14.1e100.net (142.250.74.238): icmp_seq=1 ttl=118 time=11.9 ms
64 bytes from par10s40-in-f14.1e100.net (142.250.74.238): icmp_seq=2 ttl=118 time=13.0 ms
^C
--- google.com ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 11.920/12.468/13.016/0.548 ms
````
🌞**Analyse de trames**

- effectuez un `ping 8.8.8.8` depuis `john`
- capturez le ping depuis `john` avec `tcpdump`
- analysez un ping aller et le retour qui correspond et mettez dans un tableau :

| ordre | type trame | IP source          | MAC source                | IP destination | MAC destination    |     
|-------|------------|--------------------|---------------------------|----------------|--------------------|
| 1     | ping       | `john` `10.3.1.11` | `john` `08:00:27:9c:82:3a`| `8.8.8.8`      | `08:00:27:91:9d:a9`|
| 2     | pong       | `8.8.8.8`          | `08:00:27:91:9d:a9`       | `10.3.1.11`    | `08:00:27:9c:82:3a`|

[trames](dossier_photo/trames_ping_8.8.8.8.pcapng)

## III. DHCP

On reprend la config précédente, et on ajoutera à la fin de cette partie une 4ème machine pour effectuer des tests.

| Machine  | `10.3.1.0/24`              | `10.3.2.0/24` |
|----------|----------------------------|---------------|
| `router` | `10.3.1.254`               | `10.3.2.254`  |
| `john`   | `10.3.1.11`                | no            |
| `bob`    | oui mais pas d'IP statique | no            |
| `marcel` | no                         | `10.3.2.12`   |

```schema
   john               router              marcel
  ┌─────┐             ┌─────┐             ┌─────┐
  │     │    ┌───┐    │     │    ┌───┐    │     │
  │     ├────┤ho1├────┤     ├────┤ho2├────┤     │
  └─────┘    └─┬─┘    └─────┘    └───┘    └─────┘
   john        │
  ┌─────┐      │
  │     │      │
  │     ├──────┘
  └─────┘
```

### 1. Mise en place du serveur DHCP

🌞**Sur la machine `john`, vous installerez et configurerez un serveur DHCP** (go Google "rocky linux dhcp server").

````
[quentin@localhost /]$ journalctl -xeu dhcpd.service
Oct 13 15:06:52 localhost.localdomain systemd[1]: Starting DHCPv4 Server Daemon...
Oct 13 15:06:52 localhost.localdomain dhcpd[1924]: Server starting service.
Oct 13 15:06:52 localhost.localdomain systemd[1]: Started DHCPv4 Server Daemon
````
````
[quentin@localhost ~]$ ip a
2: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:08:44:06 brd ff:ff:ff:ff:ff:ff
    inet 10.3.1.2/24 brd 10.3.1.255 scope global dynamic noprefixroute enp0s8
````
🌞**Améliorer la configuration du DHCP**
  - il doit connaître l'adresse d'un serveur DNS pour avoir de la résolution de noms
    - vérifier avec la commande `dig` que ça fonctionne
    - vérifier un `ping` vers un nom de domaine
````
[quentin@localhost ~]$ ip a
2: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:08:44:06 brd ff:ff:ff:ff:ff:ff
    inet 10.3.1.2/24 brd 10.3.1.255 scope global dynamic noprefixroute enp0s8
````
````
[quentin@localhost ~]$ ping 10.3.1.254
PING 10.3.1.254 (10.3.1.254) 56(84) bytes of data.
64 bytes from 10.3.1.254: icmp_seq=1 ttl=64 time=0.639 ms
64 bytes from 10.3.1.254: icmp_seq=2 ttl=64 time=0.903 ms
64 bytes from 10.3.1.254: icmp_seq=3 ttl=64 time=0.584 ms
^C
--- 10.3.1.254 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2021ms
rtt min/avg/max/mdev = 0.584/0.708/0.903/0.139 ms
````
````
[quentin@localhost ~]$ ip r s
default via 10.3.1.254 dev enp0s8 proto dhcp src 10.3.1.2 metric 100
10.3.1.0/24 dev enp0s8 proto kernel scope link src 10.3.1.2 metric 100
````
````
[quentin@localhost ~]$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=112 time=23.9 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=112 time=24.2 ms
^C
--- 8.8.8.8 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 23.899/24.062/24.225/0.163 ms
````
````
[quentin@localhost ~]$ dig google.com
;; ANSWER SECTION:
google.com.             300     IN      A       216.58.209.238
````
````
[quentin@localhost ~]$ ping google.com
PING google.com (216.58.209.238) 56(84) bytes of data.
64 bytes from par10s29-in-f238.1e100.net (216.58.209.238): icmp_seq=1 ttl=247 time=29.0 ms
64 bytes from par10s29-in-f14.1e100.net (216.58.209.238): icmp_seq=2 ttl=247 time=22.9 ms
^C
--- google.com ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 22.884/25.957/29.030/3.073 ms
````

### 2. Analyse de trames

🌞**Analyse de trames**

- lancer une capture à l'aide de `tcpdump` afin de capturer un échange DHCP
- demander une nouvelle IP afin de générer un échange DHCP
- exportez le fichier `.pcapng`

[trames](trames_dhcp_tp3.pcapng)