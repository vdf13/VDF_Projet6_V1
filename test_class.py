# -*- coding: utf-8 -*-

# Test de copie de texte
import os

class DhcpInterface:
	""" Classe qui va créer l'objet fichier isc-dhcp-server
	Attributs de cette classe :
	- nom du fichier qui sera créé
	- valeur de la clé cherché dans le dictionnaire
	- valeur 

	"""
	def __init__(self, input_yml={}):
		""" Création des attributs de l'objet fichier isc-dhcp-server """
		self.file_name = "C:\\01_DATA\\PYTHON\\VDF_P6\\isc-dhcp-server"
		self.key_interfaceV4 = 'dhcp_interface'
		self.key_interfaceV6 = 'dhcp_interface'
		self.text_interfaceV4 = 'INTERFACES="' + input_yml[self.key_interfaceV4] + '"'
		self.text_to_write = ''
		self.input_yml = input_yml


		if self.key_interfaceV4 in self.input_yml:
			self.write(self.text_interfaceV4)
			
	def write(self, text_to_add):
		""" Méthode pour écrire le texte dans le fichier """
		if self.text_to_write != "":
			self.text_to_write += "\n"
		self.text_to_write += text_to_add
		return self.text_to_write

class DhcpConf:
	""" Classe qui va créer l'objet fichier dhcpd.conf
	Attributs de cette classe :
	- nom du fichier qui sera créé
	- valeur de la clé cherché dans le dictionnaire
	- Texte formaté a écrire 

	"""
	def __init__(self, input_yml={}, **donnees):
		""" Création des attributs de l'objet Dhcpd.conf """
		self._default_value = {
		'default-lease-time': '600',
		'max-lease-time': '7200',
		'option subnet-mask': '',
		'option broadcast-address': '',
		'option routers': '',
		'option domain-name-servers1': '', 
		'option domain-name-servers2': '',
		'authoritative': '#autoritative',
		'option ntp-servers': '',
		'option domain-name': 'example.org'
		}
		self.file_name = "C:\\01_DATA\\PYTHON\\VDF_P6\\dhcpd.conf"
	

		self.text_to_write = ''
		self.input_yml = input_yml
		modified_yml = input_yml.copy()

		for cle in input_yml:
			if cle not in self._default_value:
				del modified_yml[cle]

		self._default_value.update(modified_yml)
		print(self._default_value)
	





	def write(self, text_to_add):
		""" Méthode pour écrire le texte dans le fichier """
		if self.text_to_write != "":
			self.text_to_write += "\n"
		self.text_to_write += text_to_add
		return self.text_to_write











class DictInputYaml(dict):
	""" Classe qui va créer l'objet dictionnaire avec les clés et valeurs du fichier yaml
	Attributs de cette classe
	- objet dict
	- représentation sous forme dictionnaire
	"""

	def __init__(self, base={},):
		self._cles = []
		self._valeurs = []
		return 

	# trouver moyen de convertir du teste str en valeur pour dict

# fonction nettoyage de texte et renvoie un dictionnaire
def cleaning_yml(data):
	""" Fonction de traitement du texte du fichier yaml
	- enlève les "---" du début du fichier
	- enlève les retours lignes "\n"
	- enlève les "- " du début de ligne
	- sépare la ligne sur le signe ":" et renvoie un dictionnaire
	"""
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

# Partie pour écrire le résultat dans un fichier
def ecrire_fichier(monfichier, contenu):
	try:
		with open(monfichier, "w") as file_to_close:
			file_to_close.write(contenu)
	except:
		print("Erreur d'écriture du fichier {} ".format(monfichier))
		file_to_close.close()



# partie test objet DictInputYaml
file_2 = "C:\\01_DATA\\PYTHON\\VDF_P6\\test_data_class"
contenu = ouverture(file_2)
#print("avant formatage \n",contenu)
# test enlever du texte
final = cleaning_yml(contenu)
#print("après formatage , le dictionnaire créé \n",final)	

# partie test objet DhcpInterface
file = DhcpInterface(input_yml = final)
print(file.file_name)
#print(file.key_interfaceV4)
#print(file.text_interfaceV4)
print(file.text_to_write)

# partie test objet DhcpConf
test = DhcpConf(final)






ecrire_fichier(file.file_name, file.text_to_write)

# essais de création d'un dictionnaire, ne semble plu utile avec la fonction cleaning

#entree = DictInputYaml()
#print("\n contenu du dict entree :",entree)


