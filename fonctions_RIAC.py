# -*- coding: utf-8 -*-
""" Fontion destiné à l'ouverture de fichier yml 

- se positionne dans le répertoire défini
- ouvre les fichiers yml présent
- gère les erreurs de répertoire non disponible
- gère les erreurs de fichiers corrompus

"""

import os

aa = "C:\\01_DATA\\PYTHON\\VDF_P6\\un_fichier.yml"
bb = "C:\\01_DATA\\PYTHON\\VDF_P6\\un_fichier2.yml"
cc = "C:\\01_DATA\\PYTHON\\VDF_P6\\autre_fichier.yml"
dd = "C:\\01_DATA\\PYTHON\\VDF_P6\\b_error_a_supprimer.yml" # erreur

# Définir la fonction ouverture qui est appelé avec comme argument le nom du fichier
def ouverture(monfichier):
	try:
		with open(monfichier, "r") as file_opened:
			contenu = file_opened.read()
			print(contenu)
			#return file_opened.read()
			return contenu
	except FileNotFoundError:
		print("Le fichier {} n'est pas accessible. ".format(monfichier))
	except UnicodeDecodeError:
		print("Problème lors de l'ouverture du fichier : {} ".format(monfichier))
		file_opened.close()
	except:
		print("Autre erreur")

def installation():
	""" Le but de cette methode est d'installer un role sur un serveur
	
	- Détecte le nom du rôle et IP du serveur dans le fichier YAML
	- Se connecte sur le serveur en ssh avec compte admin
	- Installe le role suivant commandes du template

	"""

def configuration():
	""" Le but de cette méthode est de configurer le rôle sur un serveur suite à l'installation.
	
	- Détecte le nom du rôle et IP du serveur dans le fichier YAML
	- Se connecte sur le serveur en ssh avec compte admin
	- Configure le serveur en fonction des éléments récupéré du fichier YAML

	"""

	# ouvrir le fichier et récupérer dans un dictionnaire les données
	contenu = ouverture(monfichier)
	


def tests():
	""" Le but de cette méthode est de tester que le serveur installé et configuré est opérationnel.

	- Détecte le nom du rôle et IP du serveur dans le fichier YAML
	- Se connecte sur le serveur en ssh avec compte admin 
	- Lance les tests en fonction des éléments présent dans le fichier YAML

	"""


def connexion_IP():
	""" Le but de cette méthode est d'établir une connexion ssh avec le serveur

	- Détecte le nom du rôle et IP du serveur dans le fichier YAML
	- Se connecte sur le serveur en ssh avec compte admin 

	"""












