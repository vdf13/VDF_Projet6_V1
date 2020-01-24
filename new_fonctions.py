# -*- coding: utf-8 -*-
# Sous linux penser à mettre le chemin de l'interpeteur Python

import os




# LES CLASSES

class Dns:
	""" création de l'objet Dns
	- En cours de dévellopement

	"""

	def __init__(self, entree={}, text_to_write='', *donnees):
		self.input_file = "C:\\01_DATA\\PYTHON\\VDF_P6\\dns_named.conf_template"
		self.output_file = "C:\\01_DATA\\PYTHON\\VDF_P6\\named.conf"
		self.text_to_write = text_to_write
		self.default_dict = {'TTL': 'val1', 'ORIGIN': 'val2'}
		self.local_keys = ['TTL', 'ORIGIN']
		self.donnees = donnees
		self.entree = entree
		self.lines = ouverture(self.input_file)

		for key in self.local_keys:
			if key in self.entree:
				self.default_dict[key] = self.entree[key]
		self.substitue()

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
						texte += line[:cc] + val + " " + self.default_dict[val] + self.end_line
						break # Important pour finir la condition
				else:
					texte += line + "\n"

		self.text_to_write = texte
		ecrire_fichier(self.output_file, self.text_to_write)

	def load_file():
		# load base as yml file
		pass

	def convert_dict(self):
		# convert default_dict with values from base dict
		pass

	def write_file(self):
		# write the result of the replace_template to the output_file
		pass

	def replace_template(self):
		# load file_template and search for key
		pass

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
		self.default_dict = { "option domain-name ": "exemple.org", \
		 "option domain-name-servers": "8.8.8.8, 8.8.4.4", \
		  "default-lease-time": "600", \
		  "max-lease-time": "7200", \
		  "authoritative": "#authoritative" \
		  }
		self.text_to_write = text_to_write
		self.lines = ouverture(self.input_file)
		self.entree = entree
		# liste des clés 
		self.local_keys = ["option domain-name ", \
		 "option domain-name-servers", \
		 "default-lease-time", \
		 "max-lease-time", \
		 "authoritative" \
		 ]
		self.end_line = ";\n"

		for key in self.local_keys:
			if key in self.entree:
				self.default_dict[key] = self.entree[key]
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
						texte += line[:cc] + val + " " + self.default_dict[val] + self.end_line
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
	
	cleaning = []
	cleaned = {}
	for texte in data:
		if texte.startswith("# "): # Pour ne pas tenir compte des lignes commençant par 
			pass
		else:
			texte = texte.replace("---", "")
			texte = texte.replace("- ", "")
			texte = texte.strip()
			cleaning.append(texte.replace("\n", ""))
			if "---" in cleaning:
				cleaning.remove("---")
			elif "" in cleaning:
				cleaning.remove("")
		

	for texte in cleaning: # on sépare chaque ligne du texte pour remplir le dictionnaire
		split = texte.split(":")
		cleaned[split[0]] = split[1].strip()
	return cleaned			

def subnet_dhcp(default_dict):
	""" Complémént de la partie subnet dans le fichier dhcpd.conf
	- récupère le dictionnaire modifié
	- crée la partie subnet 
	- retour du texte à la classe pour écriture du fichier dhcpd.conf
	- variables : IP_subnet, IP_netmask, IP_range_start, IP_range_stop, IP_router, IP_broadcast

	"""
	IP_subnet = default_dict['IP_subnet']
	IP_netmask = default_dict['IP_netmask']
	IP_range_start = default_dict['IP_range_start']
	IP_range_stop = default_dict['IP_range_stop']
	IP_router = default_dict['IP_router']
	IP_broadcast = default_dict['IP_broadcast']
	IP_subnet = default_dict['IP_subnet']

	template_subnet = "subnet" + \
	 IP_subnet + \
	 "netmask" + \
	 IP_netmask + \
	 "{\n" + \
	 "range" + \
	 IP_range_start + \
	 IP_range_stop + \
	 ";\n" + \
	 "option routers" + \
	 IP_router + \
	 ";\n" + \
	 "option broadcast-address" + \
	 IP_broadcast + \
	 ";\n" + \
	 "}"



