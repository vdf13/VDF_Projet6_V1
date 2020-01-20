# -*- coding: utf-8 -*-

# Test de copie de texte
import os

class Da:
	""" Classe qui va créer l'objet fichier modifiable
	Attributs de cette classe :
	- nom fichier, carac, dico defaut
	- méthode , se créer, lire, modifier, écrire texte
	
	"""
	def __init__(self, entree={}, text_to_write=''):
		""" Création des attributs de l'objet  """
		self.file_name = "C:\\01_DATA\\PYTHON\\VDF_P6\\Da"
		self.def_dict = { "a": "A", "b": "B", "d": "D", "e": "E"}
		self.text_to_write = text_to_write
		self.entree = entree
		# liste des clés 
		self.local_keys = ["a", "b", "d", "e"]

		


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
		print("avant", self.text_to_write)
		texte =''
		lines = self.text_to_write.splitlines()
		#print(lines)
		for line in lines:
			if str(line).startswith("#") is False:
				for val in self.local_keys:
					if val in line:
						texte += val + " " + self.def_dict[val] + "\n"
						

				
			else:
				texte += line + "\n"



		print("après text_to_write :\n", self.text_to_write)
		print("après texte : \n", texte)
		self.write

		




# début phase de test
local = {"a": "x", "b": "B", "c": "C", "d": "D", "e": "x", "f": "xx"}
modele = "#Voici mon texte\n# Diese\n# Diese\na\nb\nTexte c\n# Encore Diese"
tdef = Da()
tnew = Da(local, modele)
print("commande print t par défaut  : ", tdef.def_dict)
print("commande print t new  : ", tnew.def_dict)
tnew.update()
print("commande print t new  après update : ", tnew.def_dict)
#print(tnew.text_to_write)
tnew.substitue()
