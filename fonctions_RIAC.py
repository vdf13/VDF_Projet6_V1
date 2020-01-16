# -*- coding: utf-8 -*-
# Sous linux penser à mettre le chemin de l'interpeteur Python


import os


# Définir la fonction ouverture qui est appelé avec comme argument le nom du fichier
def ouverture(monfichier):
	""" Fontion destiné à l'ouverture de fichier yml 

	- se positionne dans le répertoire défini
	- ouvre les fichiers yml donné en entrée
	- retourne les données du fichier lu
	- gère les erreurs de lecture de fichiers

	"""
	try:
		with open(monfichier, "r") as file_opened:
			contenu = file_opened.read()
			#return file_opened.read()
			return contenu
	except FileNotFoundError:
		print("Le fichier {} n'est pas accessible. ".format(monfichier))
	except UnicodeDecodeError:
		print("Problème lors de l'ouverture du fichier : {} ".format(monfichier))
		file_opened.close()
	except:
		print("Autre erreur")
#  Penser à écrire le fichier log


def installation():
	""" Le but de cette methode est d'installer un role sur un serveur
	
	- Détecte le nom du rôle et IP du serveur dans le fichier YAML
	- Se connecte sur le serveur en ssh avec compte admin
	- Installe le role suivant commandes du template

	"""

#  Penser à écrire le fichier log

def configuration():
	""" Le but de cette méthode est de configurer le rôle sur un serveur suite à l'installation.
	
	- Détecte le nom du rôle et IP du serveur dans le fichier YAML
	- Se connecte sur le serveur en ssh avec compte admin
	- Configure le serveur en fonction des éléments récupéré du fichier YAML

	"""

	# ouvrir le fichier et récupérer dans un dictionnaire les données
	contenu = ouverture(monfichier)

#  Penser à écrire le fichier log

def tests():
	""" Le but de cette méthode est de tester que le serveur installé et configuré est opérationnel.

	- Détecte le nom du rôle et IP du serveur dans le fichier YAML
	- Se connecte sur le serveur en ssh avec compte admin 
	- Lance les tests en fonction des éléments présent dans le fichier YAML

	"""

#  Penser à écrire le fichier log

def connexion_IP():
	""" Le but de cette méthode est d'établir une connexion ssh avec le serveur

	- Détecte le nom du rôle et IP du serveur dans le fichier YAML
	- Se connecte sur le serveur en ssh avec compte admin 

	"""
#  Penser à écrire le fichier log

def ecrire_fichier(monfichier, contenu):
	""" Le but de cette méthode est d'écrire le fichier configuration ou log

	- monfichier sera le fichier qui sera écrit
	- contenu les données de ce fichier

	"""
	try:
		with open(monfichier, "w") as file_to_close:
			file_to_close.write(contenu)
	except:
		print("Erreur d'écriture du fichier {} ".format(monfichier))
		file_to_close.close()
#  Penser à écrire le fichier log

def configuration_role(traitement, role_demande):
	""" Methode pour configurer les rôles détecté dans le fichier yaml

	- partie du fichier traité en argument
	- role choisi en argument

	"""
	if role_demande == 'dhcp':
		configuration_dhcp(traitement)
	elif role_demande == 'dns':
		configuration_dns(traitement)
	elif role_demande == 'apache':
		configuration_apache(traitement)
	else:
		print("Aucun rôle défini !? ")

def configuration_dhcp(traitement):
	""" Fonction qui va générer les fichiers de configuration du rôle dhcp

	- traitement est la partie du fichier qui concerne le dhcp
	- renvoie 2 fichiers de configuration
	- /etc/init.d/isc-dhcp-server
	- /etc/dhcp/dhcpd.conf

	"""
	file_1 = "C:\\01_DATA\\PYTHON\\VDF_P6\\isc-dhcp-server" # chemin à modifier ultérieurement
	file_2 = "C:\\01_DATA\\PYTHON\\VDF_P6\\dhcpd.conf" # chemin à modifier ultérieurement
	if 'dhcp_interface' in traitement:
		texte_to_write = traitement['dhcp_interface']  # Doublon a voir si besoin de garder
		line_to_write = "INTERFACEV4=" + '"' + traitement['dhcp_interface'] + '"'
		print(line_to_write)
		ecrire_fichier(file_1, line_to_write)
		print("le fichier {0} viens d'être créé avec la/les valeurs : {1} ".format(file_1, line_to_write))
	

	else:
		print("Il manque dans le fichier de configuration le parametre dhcp_interface ")


def configuration_dns(traitement):
	print

def configuration_apache(traitement):
	print











