# -*- coding: utf-8 -*-
# Sous linux penser à mettre le chemin de l'interpeteur Python

import os




# LES CLASSES

class DhcpdConf:
	""" Classe qui va créer l'objet fichier dhcpd.conf
	Attributs de cette classe :
	- nom fichier entrée et sortie
	- dictionnaire des valeurs par defaut si pas transmis en valeur entree, c'est le parametre par défaut qui est pris
	- liste des clés de l'objet = local_keys   la conversion de valeurs ne se fait que sur les clés de cette liste
	- méthodes : se créer,  écrire texte, substituer texte de input_file
	
	"""
	def __init__(self, entree={}, text_to_write=''):
		""" Création des attributs de l'objet  """
		self.output_file = "C:\\01_DATA\\PYTHON\\VDF_P6\\dhcpd.conf"
		self.input_file = "C:\\01_DATA\\PYTHON\\VDF_P6\\dhcpd.conf_template_debian"
		self.def_dict = { "option domain-name ": "AAAAAA", "option domain-name-servers": "BBBBBBB, 222222", "default-lease-time": "DDDDDDDD"}
		self.text_to_write = text_to_write
		self.lines = ouverture(self.input_file)
		self.entree = entree
		# liste des clés 
		self.local_keys = ["option domain-name ", "option domain-name-servers", "default-lease-time"]
		self.end_line = ";\n"

		for key in self.local_keys:
			if key in self.entree:
				self.def_dict[key] = self.entree[key]
		self.substitue()
	
	def write(self, text_to_add=''):
		""" Méthode pour écrire le texte dans le fichier """
		if self.text_to_write != "":
			self.text_to_write += "\n"
		self.text_to_write += text_to_add
		return self.text_to_write	

	def substitue(self):
		""" Méthode qui va remplacer dans le texte les valeurs modifiés ou défaut"""
		texte =''
		#lines = self.text_to_write.splitlines()
		# lines = self.text_to_write
		#print(lines)
		for line in self.lines:
			if str(line).startswith("#") is True:
				# cas ou il y a un # en début de ligne, on recopie la ligne
				texte += line + "\n"								
			else:
				# Cas ou la ligne ne commence pas par #
				for val in self.local_keys:
					if val in line:
						cc = line.find(val, 0, len(line))
						texte += line[:cc] + val + " " + self.def_dict[val] + self.end_line
						break # Important pour finir la condition
				else:
					texte += line + "\n"

		self.text_to_write = texte
		ecrire_fichier(self.output_file, self.text_to_write)


# LES FONCTIONS

# Définir la fonction ouverture du fichier yml ligne par ligne pour envoie à la fonction cleaning_yml
def ouverture_yml(monfichier):
	try:
		with open(monfichier, "r") as file_opened:
			contenu = file_opened.readlines()
			return contenu
	except:
		print("Autre erreur")

def ouverture(monfichier):
	""" ouverture des fichiers en mode ligne par ligne """
	# voir si pas doublon avec le fonction ouverture_yml qui est aussi en mode ligne
	try:
		with open(monfichier, "r") as file_opened:
			contenu = file_opened.readlines()
			return contenu
	except:
		print("Autre erreur")

def ecrire_fichier(monfichier, contenu):
	try:
		with open(monfichier, "w") as file_to_close:
			file_to_close.write(contenu)
	except:
		print("Erreur d'écriture du fichier {} ".format(monfichier))
		file_to_close.close()



# fonction nettoyage de texte et renvoie un dictionnaire. Associé à la fonction ouverture_yml
def cleaning_yml(data):
	""" Fonction de traitement du texte du fichier yaml
	- enlève les "---" du début du fichier
	- enlève les retours lignes "\n"
	- enlève les "- " du début de ligne
	- sépare la ligne sur le signe ":" et renvoie un dictionnaire
	"""
	"""
	cleaning = []
	cleaned = {}
	for texte in data:
		texte = texte.replace("- ", "")
		cleaning.append(texte.replace("\n", ""))
		print(cleaning)
		if "---" in cleaning:
			cleaning.remove("---")
		elif "" in cleaning:
			cleaning.remove("")
		elif "# " in cleaning:
			cleaning.remove()
		
	for texte in cleaning:
		split = texte.split(":")
		cleaned[split[0]] = split[1].strip()
	return cleaned
	"""
	# nouvelle tentative codage
	cleaning = []
	cleaned = {}
	for texte in data:
		if texte.startswith("# "): # Pour ne pas tenir compte des lignes commençant par 
			pass
		else:
			texte = texte.replace("- ", "")
			cleaning.append(texte.replace("\n", ""))
			if "---" in cleaning:
				cleaning.remove("---")
			elif "" in cleaning:
				cleaning.remove("")

	for texte in cleaning: # on sépare chaque ligne du texte pour remplir le dictionnaire
		split = texte.split(":")
		cleaned[split[0]] = split[1].strip()
	return cleaned			


