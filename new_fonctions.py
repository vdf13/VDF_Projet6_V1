#!/usr/bin/python2.7
# -*- coding: utf-8 -*-


import os
import yaml
import re





# LES CLASSES
class Dns2:
	""" création de l'objet Dns
	- En cours de dévellopement

	"""

	def __init__(self, entree={}, text_to_write=''):
		#self.input_file = "/home/administrateur/VDF_P6/dns_named.conf_template"
		self.input_file = "/home/administrateur/VDF_P6/dns_ztest"
		self.output_file = "/home/administrateur/VDF_P6/db.test.dns"
		self.text_to_write = text_to_write
		self.default_dict = {\
		'domain_name': 'serveur.exemple.org', \
		'domain_IP': '66.77.88.99', \
		'www_IP': '100.101.102.103', \
		'domain_email': 'webmaster.serveur.exemple.org', \
		'TTL': '604800', \
		'ORIGIN': 'example.org', \
		'serial': 'date_jour', \
		'refresh': "3600 ou 1H", \
		'retry': '1200 ou 15M', \
		'expire': '2592000 ou 1m'\
		}
		self.with_dollar = ('ORIGIN', 'TTL')
		self.with_SOA= ('serial', 'refresh', 'retry', 'expire')
		self.entree = entree
		self.template = ouverture(self.input_file)

		for key in self.entree.keys():
			self.default_dict[key] = entree[key]
		#print(self.default_dict)

		# on apelle la fonction de remplacement du texte
		self.substitue()

	def substitue(self):
		'''
		Fonction qui remplace dans le texte template les valeur du dictionnaire par défaut modifé
		- fichier entrée yaml
		- dictionnaire par défaut
		'''
		
		#regexp = '[ ]([\w"., -/]*)' # key+_.," en fait jusque trouver le ;
		#regexp = '[ ]([\w., -]*)' # key+_.," en fait jusque trouver le ; enlevé [ ]?
		regexp2 = '[\d\w]*\s;\s' # pour forwarders
		#regexp3 = '[\t\s]+.*'	# marche pour tab après TTL	
		regexp = '\$'

		#print(self.template)
		for key in self.default_dict:
			
			if key in self.template:
				
				#print(key, self.default_dict[key])
				if key in self.with_dollar:
					#print("key in $$$$$$$$$ = ", key)
					#print("trouve ?", re.search(r"{0}{1}[\t \w\d]*".format(regafter, key), self.template))
					self.template = re.sub(r"{0}{1}[\t \w\d]*".format(regexp, key), '${0} {1}'.format(key, self.default_dict[key]), self.template, count=1 )
				elif key in self.with_SOA:
					self.template = re.sub(r"{0}{1}".format(regexp2, key), str(self.default_dict[key]) + " ; " + key, self.template, count=0 )
				
				else:
					self.template = re.sub(r"{0}".format(key), "{0}".format(self.default_dict[key]), self.template)
					
				self.text_to_write = self.template	
			#print("\nkey = ", key, self.default_dict[key], self.text_to_write)	# a enlever, pour debuger
			
		ecrire_fichier(self.output_file, self.text_to_write)
		#print("///////")
		#print(self.text_to_write)	# pour le debogage, a supprimer


class Dns:
	""" création de l'objet Dns
	- En cours de dévellopement

	"""

	def __init__(self, entree={}, text_to_write=''):
		#self.input_file = "/home/administrateur/VDF_P6/dns_named.conf_template"
		self.input_file = "/home/administrateur/VDF_P6/dns_named.conf_template"
		self.output_file = "/home/administrateur/VDF_P6/named.conf"
		self.text_to_write = text_to_write
		self.default_dict = {\
		'zone': 'example.org2', \
		'type': 'master', \
		'file': '/etc/bind/db.example.org', \
		'directory': "/etc/bind/", \
		'dump-file': '/var/log/named_dump.db', \
		'statistics-file': '/var/log/named.stats', \
		'forwarders': '10.0.10.254', \
		'listen-on': '53' \
		}
		self.with_quote = ('directory', 'dump-file', 'statistics-file')
		self.with_brace = ('forwarders')
		self.with_zone = ('zone', 'type', 'file')
		self.entree = entree
		self.template = ouverture(self.input_file)

		for key in self.entree.keys():
			self.default_dict[key] = entree[key]
		print(self.default_dict)

		# on apelle la fonction de remplacement du texte
		self.substitue()

	def substitue(self):
		'''
		Fonction qui remplace dans le texte template les valeur du dictionnaire par défaut modifé
		- fichier entrée yaml
		- dictionnaire par défaut
		'''
		
		#regexp = '[ ]([\w"., -/]*)' # key+_.," en fait jusque trouver le ;
		regexp = '[ ]"([\w".,-/]*)' # key+_.," en fait jusque trouver le ; enlevé [ ]?
		regexp2 = '[ ]{([\w .;]*)' # pour forwarders

		#print(self.template)
		for key in self.default_dict:
			
			if key in self.template:
				
				print(key, self.default_dict[key])
				if key in self.with_quote:
					self.template = re.sub(r"{0}{1}".format(key, regexp), '{0} "{1}"'.format(key, self.default_dict[key]), self.template, count=1 )
				elif key in self.with_brace:
					self.template = re.sub(r"{0}{1}".format(key, regexp2), key + " { " + self.default_dict[key] + "; ", self.template, count=0 )
				elif key in self.with_zone:	
					print("trouve ?", re.search(r"{0}{1}[\t \w\d]*".format(regexp, key), self.template))
					self.template = re.sub(r"{0}{1}".format(key, regexp), "{0} {1}".format(key, self.default_dict[key]), self.template, count=1)
				else:
					self.template = re.sub(r"{0}{1}".format(key, regexp), "{0} {1}".format(key, self.default_dict[key]), self.template, count=1 )
					
				self.text_to_write = self.template	
			#print("\nkey = ", key, self.default_dict[key], self.text_to_write)	# a enlever, pour debuger
			
		ecrire_fichier(self.output_file, self.text_to_write)
		
		print(self.text_to_write)	# pour le debogage, a supprimer

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
		# cette fonction pour gérer mieux le dict sur le vrai fichier yaml
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
			self.template = re.sub(r"{0}{1}".format(key, regexp), "{0} {1}".format(key, self.default_dict[key]), self.template)
			self.text_to_write = self.template
			#print(self.text_to_write[1])
		ecrire_fichier(self.output_file, self.text_to_write)
		
		#print(self.text_to_write)	# pour le debogage, a supprimer
	
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
				#print(self.text_to_write)
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
