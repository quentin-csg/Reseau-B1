# TP4 : TCP, UDP et services réseau

# Sommaire

- [TP4 : TCP, UDP et services réseau](#tp4--tcp-udp-et-services-réseau)
- [Sommaire](#sommaire)
- [0. Prérequis](#0-prérequis)
- [I. First steps](#i-first-steps)
- [II. Mise en place](#ii-mise-en-place)
  - [1. SSH](#1-ssh)
  - [2. Routage](#2-routage)
- [III. DNS](#iii-dns)
  - [2. Setup](#2-setup)
  - [3. Test](#3-test)

# 0. Prérequis

# I. First steps

🌞 **Déterminez, pour ces 5 applications, si c'est du TCP ou de l'UDP**  
🌞 **Demandez l'avis à votre OS**

- ## Client lol:  
Port serveur = 2099  
Port local = 56597   
[trames_client_lol](dossier_photo/trames_client_lol.pcapng)

````
PS C:\Windows\system32> netstat -b -n
[LeagueClientUxRender.exe]
  TCP    10.33.16.140:56597    185.40.64.65:2099      ESTABLISHED
```` 

- ## Lol in game:  
Port serveur = 5326  
Port local = 62759    
[trames_client_lol](./dossier_photo/trames_lol_ingame.pcapng)  

- ## Speedtest
Port serveur = 8080 
Port local = 60765   
[trames_client_lol](dossier_photo/trames_speedtest.pcapng)

````
PS C:\Windows\system32> netstat -b -n
[chrome.exe]
  TCP    10.33.16.140:60765     89.84.1.181:8080       ESTABLISHED
````
- ## Discord

Port serveur = 443 
Port local = 57769    
[trames_client_lol](dossier_photo/trames_discord.pcapng)

````
PS C:\Windows\system32> netstat -b -n
[Discord.exe]
  TCP    10.33.16.140:57769     162.159.128.233:443    ESTABLISHED
````

- ## Evernote

Port serveur = 443 
Port local = 53683    
[trames_client_lol](./dossier_photo/trames_evernote.pcapng)

````
PS C:\Windows\system32> netstat -b -n
[Evernote.exe]
  TCP    192.168.1.166:53683    35.188.42.15:443       TIME_WAIT
````

# II. Mise en place

## 1. SSH

🖥️ **Machine `node1.tp4.b1`**


🌞 **Examinez le trafic dans Wireshark**

- **déterminez si SSH utilise TCP ou UDP**  
  SSH utilise le TCP
- **repérez le *3-Way Handshake* à l'établissement de la connexion**  

[trames_ssh](./dossier_photo/trames_ssh.pcapng)

🌞 **Demandez aux OS**

Depuis Windows
````
PS C:\Windows\system32> netstat -b -n

Connexions actives

  Proto  Adresse locale         Adresse distante       État
  TCP    10.4.1.1:50734         10.4.1.11:22           ESTABLISHED
 [ssh.exe]
````
Depuis ma VM
````
[quentin@node1 ~]$ ss
Netid    State    Recv-Q    Send-Q                      Local Address:Port          Peer Address:Port
tcp      ESTAB    0         52                              10.4.1.11:ssh               10.4.1.1:50734
````


## 2. Routage

> Rien à remettre dans le compte-rendu pour cette partie.

# III. DNS

## 2. Setup

🖥️ **Machine `dns-server.tp4.b1`**

🌞 **Dans le rendu, je veux:**

- un `cat` des fichiers de conf

````
options {
        listen-on port 53 { 127.0.0.1; any; };
        listen-on-v6 port 53 { ::1; };
        directory       "/var/named";
        dump-file       "/var/named/data/cache_dump.db";
        statistics-file "/var/named/data/named_stats.txt";
        memstatistics-file "/var/named/data/named_mem_stats.txt";
        secroots-file   "/var/named/data/named.secroots";
        recursing-file  "/var/named/data/named.recursing";
        allow-query     { localhost; any;  };
        allow-query-cache { localhost; any; };
        recursion yes;

zone "tp4.b1" IN {
        type master;
        file "tp4.b1.db";
        allow-update { none; };
        allow-query { any; };
};

zone "1.4.10.in-addr.arpa" IN {
        type master;
        file "tp4.b1.rev";
        allow-update { none; };
        allow-query { any; };
};
````
- un `systemctl status named` qui prouve que le service tourne bien  
````
[quentin@dns-server /]$ sudo systemctl status named
● named.service - Berkeley Internet Name Domain (DNS)
     Loaded: loaded (/usr/lib/systemd/system/named.service; enabled; vendor preset: disabled)
     Active: active (running) since Tue 2022-10-25 13:45:12 CEST; 33s ago
````
- une commande `ss` qui prouve que le service écoute bien sur un port
````
[quentin@dns-server etc]$ sudo  ss -alntp
State      Recv-Q     Send-Q         Local Address:Port          Peer Address:Port     Process
LISTEN     0          10                10.4.1.201:53                 0.0.0.0:*         users:(("named",pid=1552,fd=21))
````

🌞 **Ouvrez le bon port dans le firewall**

````
[quentin@dns-server etc]$ sudo firewall-cmd --add-port=53/tcp --permanent
success
````

## 3. Test

🌞 **Sur la machine `node1.tp4.b1`**
````
[quentin@node1 ~]$ dig dns-server.tp4.b1

; <<>> DiG 9.16.23-RH <<>> dns-server.tp4.b1
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 57615
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: 9b711f49ccabe622010000006357e7290c5df5bd63baa1ad (good)
;; QUESTION SECTION:
;dns-server.tp4.b1.             IN      A

;; ANSWER SECTION:
dns-server.tp4.b1.      86400   IN      A       10.4.1.201

;; Query time: 1 msec
;; SERVER: 10.4.1.201#53(10.4.1.201)
;; WHEN: Tue Oct 25 16:22:03 CEST 2022
;; MSG SIZE  rcvd: 90
````
````
[quentin@node1 ~]$ dig google.com

; <<>> DiG 9.16.23-RH <<>> google.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 33888
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: bd516d4a8c0468ab010000006357e702a93ad2652cdcb9a2 (good)
;; QUESTION SECTION:
;google.com.                    IN      A

;; ANSWER SECTION:
google.com.             136     IN      A       216.58.214.174

;; Query time: 0 msec
;; SERVER: 10.4.1.201#53(10.4.1.201)
;; WHEN: Tue Oct 25 16:21:27 CEST 2022
;; MSG SIZE  rcvd: 83
````

🌞 **Sur votre PC**

````
PS C:\Windows\system32> nslookup node1.tp4.b1 10.4.1.201
Serveur :   dns-server.tp4.b1
Address:  10.4.1.201

Nom :    node1.tp4.b1
Address:  10.4.1.11
````

[trames](./dossier_photo/trames_rep_dns.pcapng)
