# VDF_Projet6_V1
Formation AIC, projet 6 "Participez à la vie de la communauté Open Source"

## Created by Victor DE FARIA
Started : 03/01/2020

# Nom du programme
Remote Install And Configure
fichier riac.py

# Obectif
L'objectif  de ce programme est d'installer et configurer les packages dhcp ou dns sur différents serveurs.

# Types de services gérés:
* DHCP
* DNS

# Fichier source de configuration 
Un fichier écrit en "yml" est nécessaire comme source du configurateur

# Mode opératoire de lancement du programme
le programme riac.py doit être lancé avec 2 arguments
* nom fichier 'file'.yml contenant les données
    1. dns.yml
    2. dhcp.yml
* la commande a éxecuter 
    1. connect
Vérifie que la connexion avec le serveur est possible
    2. install
Installe le package renseigné dans le fichier yaml sur le serveur
    3. configure
Configure le service renseigné dans le fichier yaml en remplaçant le fichier par défaut par les nouvelles valeurs 
    4. auto
Les 3 commandes précédentes enchainés automatiquement.
    5. test
Vérifie que le fichier .yml a les champs role_name title connect renseignés

ex : python riac.py dns.yml install


# Processus de fonctionnement du programme
    1. Lire fichier 'file'.yml et test de présence d'informations
    2. Se connecter avec IP + login (valeur du fichier)
    3. Installer le rôle (valeur du fichier)
    4. Vérifier que le package est présent
    5. Copier le fichier default du service en .origin
    6. Configurer le rôle (valeur du fichier) en modifiant le fichier default du service
    7. Ecrire le fichier dans le répertoire adéquat
    8. Ecrire le fichier log

# Fichier log
Le fichier riac.log est généré par le programme, il trace les erreurs ainsi que la réussite des étapes du programme
chemin /var/log/riac.log

# Fichier YAML
Le fichier YAML est décomposé en 3 parties:
role_name:
connect:


# Liste des erreurs générés par le programme
    2. Erreur de syntaxe lors du lancement du programme
    3. Erreur de présence, ouverture de fichiers
    4. Erreur d'écriture de fichiers, de connexion ssh
    5. Erreur d'intégrité du fichier YAML, champs mal renseignés
    6. Erreur de contrôle de l'installation
    
