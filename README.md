# VDF_Projet6_V1
Formation AIC, projet 6 "Participez à la vie de la communauté Open Source"

## Created by Victor DE FARIA
Started : 03/01/2020

# Nom du programme et composition des fichiers
Remote Install And Configure    RIAC
Composé de 2 fichiers codé en python: 
* main_RIAC.py 
* fonction_RIAC.py 
Composé de 2 fichiers entrée YAML pour service dns ou dhcp
* dns.yml
* dhcp.ymp
2 répertoires 
* /résultat   Qui acceuille les fichiers créé par le programme avant transfert au serveur
* /templates  Qui contient les fichiers modèles qui seront utilisés par le programme
- dhcpd.conf_tpl_debian
- dns_zone_tpl_debian
- dns_named.conf_tpl_debian
- isc-dhcp-server_tpl_debian
Fichier log
* riac.log


# Obectifs et pré-requis
L'objectif  de ce programme est d'installer et configurer les packages dhcp ou dns sur différents serveurs en fonction des valeurs fournies par un fichier au format YAML. Il se lance sur le poste de l'administrateur et se connecte sur les serveurs Debian.
Il permet d'automatiser la création des services et évite les erreurs de  rédaction des fichiers de configuration.
pré-requis:
* Le programme et les fichiers / répertoires doivent être installé sur le poste administrateur
* Les serveurs doivent être installés avec un compte qui a les droits sudo
* Le service serveur ssh doit être installé sur les serveurs
* La clé publique du poste administrateur doit être envoyé aux serveurs

# Types de services gérés:
* DHCP
* DNS

# Mode opératoire de lancement du programme
le programme riac.py doit être lancé avec 2 arguments
* nom fichier 'file.yml' contenant les données pour le service à installer :
    1. dns.yml
    2. dhcp.yml
* la commande a éxecuter :
    1. connect      Vérifie que la connexion avec le serveur est possible
    2. install      Installe le package renseigné dans le fichier yaml sur le serveur
    3. configure    Configure le service renseigné dans le fichier yaml en remplaçant le fichier par défaut par les nouvelles valeurs 
    4. auto         Les 3 commandes précédentes enchainés automatiquement.
    5. test         Vérifie que le fichier .yml a les champs 'role_name' 'title' 'connect' renseignés

Résultat affiché sur le terminal lors du lancement du programme fonction auto
```
administrateur@DBG-P6:~RIAC$ python3 main_RIAC.py dhcp.yml auto
Partie connexion lancé :
Partie installation lancé : role = dhcp
Partie configuration lancé : role = dhcp
dhcpd.conf    100%  967 1.6MB/s 00:00
isc-dhcp-server   100%  19     29.6MB/s 00:00
Programme RIAC correctement terminé. Fonction : auto
administrateur@DBG-P6:~RIAC$
```


# Algorithme de fonctionnement du programme
    1. Lire fichier 'file.yml' et tester la présence d'informations clés
    2. Se connecter en ssh avec login + IP   (valeur du fichier)
    3. Installer le rôle (valeur du fichier)
    4. Vérifier que le package installé est présent sur le serveur
    5. Copier le fichier configuration par default du service en fichier.origin
    6. Configurer le rôle (valeur du fichier) en modifiant le fichier modèle du service
    7. Ecrire le fichier dans le répertoire adéquat pour le service installé
    8. Ecrire le fichier log en cas de réussite des actions
    9. Ecrire le fichier log en cas d'erreurs

# Fichier log 
Le fichier riac.log est généré par le programme, il trace les erreurs ainsi que la réussite des étapes du programme
chemin $HOME/riac.log
```
25 Feb 2020 09:21 La connexion au serveur 192.168.20.32 c'est correctement effectuée.
25 Feb 2020 09:21 Le package isc-dhcp-server viens d'être installé sur le serveur 192.168.20.32 25 Feb 2020 09:21 Le fichier /tmp/dhcpd.conf à été configuré sur le serveur 192.168.20.32 .
25 Feb 2020 09:21 Le fichier /tmp/isc-dhcp-server à été configuré sur le serveur 192.168.20.32 .
25 Feb 2020 09:21 La connexion au serveur 192.168.20.32 c'est correctement effectuée.
25 Feb 2020 09:21 Programme RIAC correctement terminé. Fonction : auto
```


# Liste des erreurs générés par le programme
Les erreurs sont affichés dans le terminal et enregistré dans le fichier log.
    * Erreur 2 : Erreur de syntaxe lors du lancement du programme
    * Erreur 3 : Erreur  de présence, ouverture de fichiers
    * Erreur 4 : Erreur  d'écriture de fichiers, de connexion ssh
    * Erreur 5 : Erreur  d'intégrité du fichier YAML, champs mal renseignés
    * Erreur 6 : Erreur de contrôle de l'installation
    
# Rédaction du fichier YAML
Il comprend 4 listes principales indispensables:
* role_name     signale le role qui sera installé
* part_xxx      valeurs utiles pour la création du 1er fichier config
* part_yyy      valeurs utiles pour la création du 2eme fichier config
* connect       valeurs utiles à la connexion ssh

Exemple d'un fichier de configuration pour le service dns.
```
role_name:
  title: dns
part_dns_named:
  zone: VDF-entreprise.com
  type: master
  file: /etc/bind/db.VDF-entreprise.com
  directory: /etc/TEST
  dump-file: /var/log/TEST_dump.db
  statistics-file: /var/log/TEST.stats
  forwarders: 192.168.10.243
  listen-on: any
part_dns_zone:
  name_file: db.VDF-entreprise.com
  domain_name: VDF-entreprise.com
  domain_IP: 192.168.10.242
  www_IP: 192.168.10.241
  domain_email: admin.srv.TEST.tst
  TTL: 604800
  ORIGIN: VDF-entreprise.com
  serial:
  refresh: 3600
  retry: 3000
  expire: 2419200
connect:
  IP_connexion: 192.168.20.22
  user_connexion: admin

```

Exemple d'un fichier de configuration pour le service dhcp.
```
--- 
role_name:
  title: dhcp 
part_dhcp_conf:
  domain-name: TEST.com
  domain-name-servers: "ns1.TEST.org, ns2.TEST.org"
  routers: rt1.TEST.org, rt2.TEST.org
  default-lease-time: 400
  max-lease-time: 5000
  authoritative: authoritative
  subnet: 192.168.10.0
  netmask: 255.255.255.0
  range: 192.168.10.100 192.168.10.200
  broadcast-address: 192.168.10.255
  ntp-servers: 192.168.1.254
part_dhcp_interface:
  INTERFACES: enp0s3
connect:
  IP_connexion: 192.168.20.32
  user_connexion: admin

```



# 