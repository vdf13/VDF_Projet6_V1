# -*- coding: utf-8 -*-

import os

# Se positionner sur le répertoire ou se trouvent les fichiers yaml
try:
	os.chdir("c:/01_DATA/PYTHON/VDF_P6")  
	curent_dir = os.getcwd()
except FileNotFoundError:
	curent_dir = os.getcwd()
	print ("stop")



# Trouver un fichier terminant par yml et l'ouvrir
try:
	for file in os.listdir(curent_dir):
		if file.endswith(".yml"):
			print(os.path.join(curent_dir, file))
			# Ouvrir le fichier se terminant par yml
			file_opened = open(os.path.join(curent_dir, file), "r")
			contenu = file_opened.read()
			print(contenu)
			file_opened.close()
except UnicodeDecodeError:
	print("Problème d'ouverture du fichier : {} ".format(file))
	file_opened.close()

	

# Tester si le fichier txt ou yml est présent 

# Gérer les erreurs d'ouverture de fichier
# Si le répertoire n'est pas correct : FileNotFoundError: [WinError 2]










