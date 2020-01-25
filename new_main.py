#!/usr/bin/python2.7
# -*- coding: utf-8 -*-


#import os
from new_fonctions import *


# Création d'un dictionnaire à partir d'un fichier yaml exemple
file_yml = "/home/administrateur/VDF_P6/fichier-entree.yml"

# partie à developper pour trier dans les rôles
def choix_role(dictionnaire_yml):
	if 'role_name' in dictionnaire_yml.keys():
		role_demande = dictionnaire_yml['role_name']
		print("rôle trouvé : ", role_demande)



# création du dictionnaire avec les valeurs lu du fichier yaml
val_yml = cleaning_yml(ouverture_yml(file_yml))
choix_role(val_yml)


# création de l'objet dhcpd.conf
dhcpd = DhcpdConf(val_yml)
print("Le fichier {0} viens d'être créé avec les valeurs du fichier {1} .".format( dhcpd.output_file, file_yml))

# Test de l'objet dns  named.conf
test_dns_yml = "/home/administrateur/VDF_P6/test_dns.yml"
test_dns = cleaning_yml(ouverture_yml(test_dns_yml))
dns = Dns(test_dns)
print("Le fichier {0} viens d'être créé avec les valeurs du fichier {1}".format( dns.output_file, test_dns))

