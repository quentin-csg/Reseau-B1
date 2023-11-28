# Arp spoof et dns spoof script

## Installation des scripts

````
git clone https://gitlab.com/quentin_csg/rendu-tp-reseaux.git
````
Installer aussi le langage python et scapy.
````
sudo apt install python3 python3-scapy
````

## Usage des scripts

Depuis le répertoire lancer la commande
````
python3 arp_spoof.py
````
Ensuite choisissez sur quelle réseaux vous voulez faire le scan.  
Avant de lancer le second script, modifiez le pour choisir la cible que vous voulez avoir et l'interface sur lequel vous faites l'attaque.
````
"src host ip_victim"
````
````
net_interface = "Choose the interface"
````
Et choississez sur quelle ip vous voulez envoyer la victime.
````
rdata='Choose the ip destination'
````  
Enfin lancez ensuite le second script.
````
sudo python3 dns_spoof.py
````