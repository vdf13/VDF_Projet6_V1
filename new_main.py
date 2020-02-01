#!/usr/bin/python2.7
#-*- coding: utf-8 -*-


import os, sys, yaml
from new_fonctions import *




# partie à developper pour trier dans les rôles
'''
def choix_role(dictionnaire_yml):
	if 'role_name' in dictionnaire_yml.keys():
		role_demande = dictionnaire_yml['role_name']
		print("rôle trouvé : ", role_demande)
'''

# création de l'objet dhcpd.conf
#dhcpd = DhcpdConf(val_yml)
#print("Le fichier {0} viens d'être créé avec les valeurs du fichier {1} .".format( dhcpd.output_file, file_yml))


# variables pour ouvrir le fichier yaml avec les arguments fichier et role recherché
fichier_yml = sys.argv[1]	# nom du fichier en premier parametre
info = sys.argv[2]			# title pour lire le nom du role à configurer

# ouverture du fichier source yaml et chargement des parametres dans le dictionnaire Vars
Vars = ouverture_yml(fichier_yml)
#print(Vars['role_name'])

IP = "1.2.3.4"	# test d'affichage, a remplacer par variable ip du fichier
# Test du role trouvé dans la variable Vars et parametre lancé a l'execution ex: python.py fichier dhcp
if Vars['role_name'][info] == 'dhcp':
	print("Le rôle {0} va être configuré sur le serveur : {1}\n".format(Vars['role_name'][info], IP))
	dhcpd = DhcpdConf(Vars['role_name'])
	print("Le fichier {0} viens d'être créé avec les valeurs du fichier {1} .".format( dhcpd.output_file, fichier_yml))
	isc = IscDhcpServer(Vars['role_name'])
	print("Le fichier {0} viens d'être créé avec les valeurs du fichier {1} .".format( isc.output_file, fichier_yml))
elif Vars['role_name'][info] == 'dns':
	print("Le rôle {0} va être configuré sur le serveur : {1}\n".format(Vars['role_name'][info], IP))
	dns = Dns(Vars['role_name'])
	print("Le fichier {0} viens d'être créé avec les valeurs du fichier {1} .".format( dns.output_file, fichier_yml))
else:
	print("pas trouvé de role à installer")


