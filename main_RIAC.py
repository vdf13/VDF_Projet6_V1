# -*- coding: utf-8 -*-
""" Programme principal d'installation et de configuration des rôles"""

#import os
from fonctions_RIAC import *


aa = "C:\\01_DATA\\PYTHON\\VDF_P6\\un_fichier.yml"
bb = "C:\\01_DATA\\PYTHON\\VDF_P6\\un_fichier2.yml"
cc = "C:\\01_DATA\\PYTHON\\VDF_P6\\autre_fichier.yml"
dd = "C:\\01_DATA\\PYTHON\\VDF_P6\\b_error_a_supprimer.yml" # erreur
ee = "C:\\01_DATA\\PYTHON\\VDF_P6\\template_dhcp.yml"
ff = "C:\\01_DATA\\PYTHON\\VDF_P6\\test_ecriture"
_donnees = {
	'dhcp_definition': 
		{
		'role_name': 'dhcp',
		'dhcp_interface': 'enp0s8',
 		'serverName': 'somewebsite.com',
		'ipAddr': '192.168.0.1',
		'default-lease-time': '600',
		'max-lease-time': '7200',
		'option subnet-mask': '255.255.255.0',
		'option broadcast-address': '192.168.1.255',
		'option routers': '192.168.1.254',
		'option domain-name-servers': ['192.168.1.1', '192.168.1.2'],
		'option domain-name': 'ubuntu-fr.lan',
		'option ntp-servers': '192.168.1.254'
		}, 
	'subnet_definition':
		{
		'subnet': '192.168.1.0',
		'netmask': '255.255.255.0',
		'range': ['192.168.1.10', '192.168.1.100']
		}
   	}

  
  



# pavé sur création des variables str pour manipuler les champs
""" Mis en pause cette partie le temps de travailler sur extraction des 
données du dictionnaire.

donnee = ouverture(aa)
split_donnee = donnee.splitlines()
template = ouverture(ee)
split_template = template.splitlines()
#print(split_donnee)
#print(split_template)
#print(donnee)
"""

""" Nouvelle partie sur extraction des données du dictionnaire
pris un modèle pré-rempli pour les tests"""


theme = []		# définition d'une liste vide "theme" pour contenir les sujets
i = 0			# compteur pour boucle while de theme

for val in _donnees:
	theme.append(val)

while i < len(theme):
	print("Partie du fichier YAML analysé pour recherche de rôle : {}".format(theme[i]))
	traitement = _donnees[theme[i]]
	i += 1
	if 'role_name' in traitement:
		role_demande = traitement['role_name']
		if role_demande is 'dhcp' or role_demande is 'dns' or role_demande is 'apache':
			print("Voici le role qui sera configuré : {}".format(role_demande))
			configuration_role(traitement, role_demande)
		else:
			print("Erreur dans la syntaxe le rôle : {} n'est pas accepté. \n Choix possibles de rôles: dhcp , dns, apache".format(role_demande))
			# ecrire log
	
	else:
		print("role non trouvé dans le fichier")
		# ecrire log

""" essai 2 
# création de 2 variables qui vont contenir les parties inclusent dans le dictionnaire
for val in theme:
	partie = _donnees[val]
	chercher_role(partie, role_trouve)
	print(role_trouve)
	if role_trouve == True:
		print(role_trouve)
		print(" trouvé dans main")
		# actions a configurer
	else:
		print(role_trouve)	

		#print("role non trouvé dans la partie du fichier : {} ".format(partie))
		# ecrire log

"""
"""	
	# chercher si le role existe dans le fichier yml champ role_name
	if 'role_name' in partie:
		role_demande = partie['role_name']
		if role_demande is 'dhcp' or role_demande is 'dns':
			role_trouve = True
			print("Voici le role qui sera configuré : {}".format(role_demande))
			return(partie)
		else:
			print("Erreur dans la syntaxe le rôle : {} n'est pas accepté. \n Choix possibles de rôles: dhcp , dns".format(role_demande))
			# ecrire log
	else:
		if role_trouve == True:
			print("role en cours de configuration")
		else:
			print("role non trouvé dans le fichier")
		# ecrire log
"""
		




# test des conditions


