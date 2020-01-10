# -*- coding: utf-8 -*-

import os

# Se positionner sur le répertoire
os.chdir("c:/01_DATA/PYTHON/VDF_P6")  
curent_dir = os.getcwd()

# lister les fichiers du répertoire
list_of_files = os.listdir(curent_dir)
print(list_of_files)

# Trouver un fichier terminant par yml 
for file in os.listdir(curent_dir):
    if file.endswith(".yml"):
        file_to_open = (os.path.join(curent_dir, file))
        print(file_to_open)
        # Ouvrir le fichier se terminant par yml
        file_opened = open(file_to_open, "r")
        contenu = file_opened.read()
        print(contenu)
        file_opened.close()
   
	

# Tester si le fichier txt ou yml est présent 

# Gérer les erreurs d'ouverture de fichier










