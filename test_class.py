# -*- coding: utf-8 -*-

# Test de copie de texte
import os

class DhcpInterface:
	""" Classe qui va créer l'objet fichier isc-dhcp-server
	Attributs de cette classe :
	- nom du fichier qui sera créé
	- valeur carte interface dhcp V4
	- valeur carte interface dhcp V6

	"""
	def __init__(self, interfaceV4='', interfaceV6='', text_to_write=''):
		""" Création des attributs de l'objet fichier isc-dhcp-server """
		self.file_name = "C:\\01_DATA\\PYTHON\\VDF_P6\\isc-dhcp-server"
		self.interfaceV4 = interfaceV4
		self.interfaceV6 = interfaceV6
		self.text_to_write = text_to_write
	def write(self, text_to_add):
		""" Méthode pour écrire le texte dans le fichier """
		if self.text_to_write != "":
			self.text_to_write += "\n"
		self.text_to_write += text_to_add

class DictInputYaml(dict):
	""" Classe qui va créer l'objet dictionnaire avec les clés et valeurs du fichier yaml
	Attributs de cette classe
	- objet dict
	- représentation sous forme dictionnaire
	"""

	def __init__(self, base={},):
		self._cles = []
		self._valeurs = []

	# trouver moyen de convertir du teste str en valeur pour dict

# fonction nettoyage de texte
def cleaning_yml(data):
	cleaning = []
	cleaned = {}
	for texte in data:
		texte = texte.replace("- ", "")
		cleaning.append(texte.replace("\n", ""))
		if "---" in cleaning:
			cleaning.remove("---")
		elif "" in cleaning:
			cleaning.remove("")
	for texte in cleaning:
		split = texte.split(":")
		cleaned[split[0]] = split[1].strip()
	return cleaned


# partie pour test ouverture	
def ouverture(monfichier):
	try:
		with open(monfichier, "r") as file_opened:
			contenu = file_opened.readlines()
			#return file_opened.read()
			return contenu
	except:
		print("Autre erreur")



# partie test objet DhcpIterface
file = DhcpInterface('eth0', )
print(file.file_name)
print(file.interfaceV4)
print(file.text_to_write)

# partie test objet DictInputYaml
file_2 = "C:\\01_DATA\\PYTHON\\VDF_P6\\test_data_class"
contenu = ouverture(file_2)
print("avant formatage \n",contenu)
# test enlever du texte
final = cleaning_yml(contenu)
print("après formatage \n",final)	


entree = DictInputYaml()
print("\n contenu du dict entree :",entree)


