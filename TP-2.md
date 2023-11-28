# TP2 : Ethernet, IP, et ARP

# I. Setup IP

🌞 **Mettez en place une configuration réseau fonctionnelle entre les deux machines**
- mon ip : 192.168.1.26
- son ip : 192.168.1.25
- l'adresse de réseau : 192.168.0.0
- l'adresse de broadcast : 192.168.3.255
  

🌞 **Prouvez que la connexion est fonctionnelle entre les deux machines**

````
PS C:\Windows\system32> ping 192.168.1.25

Envoi d’une requête 'Ping'  192.168.1.25 avec 32 octets de données :
Réponse de 192.168.1.25 : octets=32 temps=1 ms TTL=128
Réponse de 192.168.1.25 : octets=32 temps=1 ms TTL=128
Réponse de 192.168.1.25 : octets=32 temps=1 ms TTL=128

Statistiques Ping pour 192.168.1.25:
    Paquets : envoyés = 3, reçus = 3, perdus = 0 (perte 0%),
Durée approximative des boucles en millisecondes :
    Minimum = 1ms, Maximum = 1ms, Moyenne = 1ms
````

🌞 **Wireshark it**

[trames](./dossier_photo/trames_ping.pcapng)

Le ping request est de type 8.
Le ping reply est de type 0.

# II. ARP my bro


🌞 **Check the ARP table**

````
PS C:\Windows\system32> arp -a

Interface : 10.33.16.140 --- 0xa
  Adresse Internet      Adresse physique      Type
  10.33.19.254          00-c0-e7-e0-04-4e     dynamique

Interface : 192.168.1.26 --- 0x15
  Adresse Internet      Adresse physique      Type
  192.168.1.25          04-d4-c4-e9-cf-8d     dynamique

  ````
🌞 **Manipuler la table ARP**
````
PS C:\Windows\system32> arp -d
PS C:\Windows\system32> arp -a

Interface : 192.168.71.1 --- 0x4
  Adresse Internet      Adresse physique      Type
  224.0.0.22            01-00-5e-00-00-16     statique

Interface : 192.168.228.1 --- 0x5
  Adresse Internet      Adresse physique      Type
  224.0.0.22            01-00-5e-00-00-16     statique

Interface : 10.33.16.140 --- 0xa
  Adresse Internet      Adresse physique      Type
  10.33.19.254          00-c0-e7-e0-04-4e     dynamique
  224.0.0.22            01-00-5e-00-00-16     statique
  255.255.255.255       ff-ff-ff-ff-ff-ff     statique

Interface : 192.168.48.1 --- 0xe
  Adresse Internet      Adresse physique      Type
  224.0.0.22            01-00-5e-00-00-16     statique

Interface : 192.168.56.1 --- 0x11
  Adresse Internet      Adresse physique      Type
  224.0.0.22            01-00-5e-00-00-16     statique

Interface : 192.168.1.26 --- 0x15
  Adresse Internet      Adresse physique      Type
  224.0.0.22            01-00-5e-00-00-16     statique
  ````

````
PS C:\Windows\system32> ping 192.168.1.25
````

````
PS C:\Windows\system32> arp -a

Interface : 192.168.71.1 --- 0x4
  Adresse Internet      Adresse physique      Type
  224.0.0.22            01-00-5e-00-00-16     statique

Interface : 192.168.228.1 --- 0x5
  Adresse Internet      Adresse physique      Type
  224.0.0.22            01-00-5e-00-00-16     statique

Interface : 10.33.16.140 --- 0xa
  Adresse Internet      Adresse physique      Type
  10.33.19.254          00-c0-e7-e0-04-4e     dynamique
  224.0.0.22            01-00-5e-00-00-16     statique
  255.255.255.255       ff-ff-ff-ff-ff-ff     statique

Interface : 192.168.48.1 --- 0xe
  Adresse Internet      Adresse physique      Type
  224.0.0.22            01-00-5e-00-00-16     statique

Interface : 192.168.56.1 --- 0x11
  Adresse Internet      Adresse physique      Type
  224.0.0.22            01-00-5e-00-00-16     statique

Interface : 192.168.1.26 --- 0x15
  Adresse Internet      Adresse physique      Type
  192.168.1.25          04-d4-c4-e9-cf-8d     dynamique
  224.0.0.22            01-00-5e-00-00-16     statique
````

🌞 **Wireshark it**

[trames](dossier_photo/trames_arp.pcapng)

Le broadcast permet d'envoyer la requête à tout le monde present sur le réseaux,
le CeLink est mon pc et Asus est le pc du receveur..

🌞 **Wireshark it**

[trames](dossier_photo/trames_dhcp.pcapng)

Your (client) IP address: 10.33.16.140

Option: (3) Router
        Lenght: 4
        Router: 10.33.19.254

Option: (6) Domain Name Server
        Lenght: 12
        Domain Name Server: 8.8.8.8
        Domain Name Server: 8.8.4.4
        Domain Name Server: 1.1.1.1