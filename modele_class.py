# -*- coding: utf-8 -*-

# Test de copie de texte
import os

class Da:
	""" Classe qui va créer l'objet fichier modifiable
	Attributs de cette classe :
	- nom fichier, carac, dico defaut
	- méthode , se créer, lire, modifier défaut, écrire texte, substituer texte
	
	"""
	def __init__(self, entree={}, text_to_write=''):
		""" Création des attributs de l'objet  """
		self.file_name = "C:\\01_DATA\\PYTHON\\VDF_P6\\dhcpd.conf"
		self.input_file = "C:\\01_DATA\\PYTHON\\VDF_P6\\dhcpd.conf_template_debian"
		self.def_dict = { "option domain-name ": "AAAAAA", "option domain-name-servers": "BBBBBBB, 222222", "default-lease-time": "DDDDDDDD"}
		self.text_to_write = text_to_write
		self.lines = ouverture(self.input_file)
		self.entree = entree
		# liste des clés 
		self.local_keys = ["option domain-name ", "option domain-name-servers", "default-lease-time"]
		self.end_line = ";\n"

		


	def update(self):
		""" Méthode qui modifie le dictionnaire des valeurs par défaut avec les valeurs reçu
		- local_keys = les clés utile à cet objet
		- def_dict = le dictionnaire avec les valeurs par défaut
		- entree = le dictionnaire extrait du fichier yaml avec les parametres à modifier
		"""
		for key in self.local_keys:
			if key in self.entree:
				self.def_dict[key] = self.entree[key]
				
	
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
		ecrire_fichier(self.file_name, self.text_to_write)

def ouverture(monfichier):
	try:
		with open(monfichier, "r") as file_opened:
			contenu = file_opened.readlines()
			#return file_opened.read()
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


# début phase de test
local = {"a": "x", "b": "B", "c": "C", "d": "D", "e": "x", "f": "xx"}
modele = "#Voici mon texte\n# Diese\n# Diese\na\nb\nTexte d\n# Encore Diese"
tdef = Da()
tnew = Da(local, modele)
print("commande print t par défaut  : ", tdef.def_dict)
print("commande print t new  : ", tnew.def_dict)

tnew.update()
print("commande print t new  après update : ", tnew.def_dict)

tnew.substitue()
print("final", tnew.text_to_write)
