# VDF_Projet6_V1
Formation AIC, projet 6 "Participez à la vie de la communauté Open Source"

## Created by Victor DE FARIA
Started : 03/01/2020

# Nom du programme
Remote Install And Configure    RIAC
fichier riac.py

# Obectif
L'objectif  de ce programme est d'installer et configurer les packages dhcp ou dns sur différents serveurs en fonction des valeurs fournies par un fichier au format YAML.

# Types de services gérés:
* DHCP
* DNS

# Fichier source de configuration YAML
Un fichier écrit en YAML "file.yml" est nécessaire comme source du configurateur.
Il comprend 4 listes principales:
* role_name     signale le role qui sera installé
* part_xxx      valeurs utiles pour la création du 1er fichier
* part_yyy      valeurs utiles pour la création du 2eme fichier
* connect       valeurs utiles à la connexion ssh


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

exemple syntaxe: python3 riac.py dns.yml install


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



# Liste des erreurs générés par le programme
    2. Erreur de syntaxe lors du lancement du programme
    3. Erreur de présence, ouverture de fichiers
    4. Erreur d'écriture de fichiers, de connexion ssh
    5. Erreur d'intégrité du fichier YAML, champs mal renseignés
    6. Erreur de contrôle de l'installation
    
# Rédaction du fichier YAML
Exemple incomplet d'un fichier de configuration pour le service dns.
Il y a les 4 listes, avec les clés et valeurs séparés par les : . L'indentation de chaque liste est a respecter.
role_name:
  title: dns
part_dns_named:
  zone: my.TEST.com
  type: master
 ....
part_dns_zone:
  domain_name: srv.TEST.tst
  domain_IP: 192.168.55.66
  ....
connect:
  IP_connexion: 192.168.20.22
  user_connexion: admin
