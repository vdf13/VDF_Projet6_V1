# -*- coding: utf-8 -*-
""" Fontion destiné à l'ouverture de fichier yml 

- se positionne dans le répertoire défini
- ouvre les fichiers yml présent
- gère les erreurs de répertoire non disponible
- gère les erreurs de fichiers corrompus

"""

import os

# Se positionner sur le répertoire ou se trouvent les fichiers yaml
try:
	os.chdir("c:/01_DATA/PYTHON/VDF_P6")  
	curent_dir = os.getcwd()
except FileNotFoundError:
	curent_dir = os.getcwd()
	print ("stop")



# Ouvre les fichiers YAML (avec l'extension yml)
try:
	for file in os.listdir(curent_dir):
		if file.endswith(".yml"):
			#print(os.path.join(curent_dir, file))
			print("Fichier en cours de traitement : {} ".format(file))
			# Ouvrir le fichier se terminant par yml
			file_opened = open(os.path.join(curent_dir, file), "r")
			contenu = file_opened.read() # Passer le contenu a une variable
			print(contenu)
			file_opened.close()
except UnicodeDecodeError:
	print("Problème lors de l'ouverture du fichier : {} ".format(file))
	file_opened.close()

	










