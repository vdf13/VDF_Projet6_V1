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










