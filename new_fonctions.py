 # -*- coding: utf-8 -*-


import os, yaml, re





# LES CLASSES

class Dns:
	""" création de l'objet Dns
	- En cours de dévellopement

	"""

	def __init__(self, entree={}, text_to_write='', *donnees):
		self.input_file = "/home/administrateur/VDF_P6/dns_named.conf_template"
		self.output_file = "/home/administrateur/VDF_P6/named.conf"
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
	- méthodes : se créer, substituer texte, écrire texte pour ajout de lignes 
	"""

	def __init__(self, entree={}, text_to_write=''):
		""" Création des attributs de l'objet  """
		self.output_file = "/home/administrateur/VDF_P6/dhcpd.conf"
		self.input_file = "/home/administrateur/VDF_P6/dhcpd.conf_template_debian"
		self.default_dict = { "domain-name": "exemple.org", \
		 "domain-name-servers": "8.8.8.8, 8.8.4.4", \
		  "default-lease-time": "600", \
		  "max-lease-time": "7200", \
		  "routers": "routeur1.exemple.org, routeur2.exemple.org", \
		  "authoritative": "#authoritative", \
		  "subnet": "172.16.100.0", \
  		  "range": "172.16.100.10 172.16.100.20" \
  		  }
	
		self.text_to_write = text_to_write
		self.template = ouverture(self.input_file)
		self.entree = entree
		
		
		# on remplace le dictionnaire par défaut par les valeurs chargées //// Poursuivre
		# cette fonction pour gérer miexu le dict sur le vrai fichier yaml
		for key in self.entree.keys():
			self.default_dict[key] = entree[key]
					
		# on apelle la fonction de remplacement du texte
		self.substitue()

	
	def substitue(self):
		'''
		Fonction qui remplace dans le texte template les valeur du dictionnaire par défaut modifé
		- fichier entrée yaml
		- dictionnaire par défaut
		'''
		
		regexp = '[ ]([\w"., -]*)' # key+_.," en fait jusque trouver le ;

		for key in self.default_dict:
			if key in self.template:
				self.text_to_write = re.sub(r"{0}{1}*".format(key, regexp), "{0} {1}".format(key, self.default_dict[key]), self.template)
		
		ecrire_fichier(self.output_file, self.text_to_write)
		print(self.text_to_write)	# pour le debugage, a supprimer
	
	def write(self, text_to_add=''):
		""" Méthode pour écrire le texte dans le fichier """
		if self.text_to_write != "":
			self.text_to_write += "\n"
		self.text_to_write += text_to_add
		return self.text_to_write	

class IscDhcpServer:
	""" Class qui va créer le fichier isc-dhcp-server avec la carte interface"""
	def __init__(self, entree={}, text_to_write=''):
		self.output_file = "/home/administrateur/VDF_P6/isc-dhcp-server"
		self.input_file = "/home/administrateur/VDF_P6/isc-dhcp-server_template_debian"
		self.default_dict = { "INTERFACES": "eth0"}
		self.entree = entree
		self.text_to_write = text_to_write
		try:
			if "INTERFACES" in self.entree.keys():
				self.text_to_write = 'INTERFACES="{0}"'.format(self.entree["INTERFACES"])
				print(self.text_to_write)
				ecrire_fichier(self.output_file, self.text_to_write)

			else:
				print("Pas trouvé la carte Interface dans le fichier ")
		except:
			print("erreur")

# LES FONCTIONS

# Définir la fonction ouverture du fichier yml ligne par ligne pour envoie à la fonction cleaning_yml
def ouverture_yml(monfichier):
	with open(monfichier, "r") as file_opened:
		try:
			return yaml.safe_load(file_opened)
		except yaml.YAMLError as exc:
			print(exc)

def ouverture(monfichier):
	""" ouverture des fichiers en mode ligne par ligne """
	try:
		with open(monfichier, "r") as file_opened:
			contenu = file_opened.read()
			return contenu
	except:
		print("Autre erreur")



def ecrire_fichier(monfichier, contenu):
	# une fois le fichier template modifié, il est créé
	try:
		with open(monfichier, "w") as file_to_close:
			file_to_close.write(contenu)
	except:
		print("Erreur d'écriture du fichier {} ".format(monfichier))
		file_to_close.close()
