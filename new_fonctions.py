#!/usr/bin/python2.7
# -*- coding: utf-8 -*-


import os
import yaml
import re
import sys
import paramiko
import time



log_file = "/home/administrateur/VDF_P6/resultat/riac.log"

# LES CLASSES
class Dns2:
	""" création de l'objet Dns
	- En cours de dévellopement

	"""

	def __init__(self, entree={}, text_to_write=''):
		#self.input_file = "/home/administrateur/VDF_P6/dns_named.conf_template"
		self.input_file = "/home/administrateur/VDF_P6/template/dns_zone_tpl_debian"
		self.output_file = "/home/administrateur/VDF_P6/resultat/db.test.dns"
		self.text_to_write = text_to_write
		self.default_dict = {\
		'domain_name': 'serveur.exemple.org', \
		'domain_IP': '66.77.88.99', \
		'www_IP': '100.101.102.103', \
		'domain_email': 'webmaster.serveur.exemple.org', \
		'TTL': '604800', \
		'ORIGIN': 'example.org', \
		'serial': 'date_jour', \
		'refresh': "3600", \
		'retry': '1200', \
		'expire': '2592000'\
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
		self.input_file = "/home/administrateur/VDF_P6/template/dns_named.conf_tpl_debian"
		self.output_file = "/home/administrateur/VDF_P6/resultat/named.conf"
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
		regexp = '[ ]"([\w".,-/]*)' # key+_.," en fait jusque trouver le ; enlevé [ ]?
		regexp2 = '[ ]{([\w .;]*)' # pour forwarders

		#print(self.template)
		for key in self.default_dict:
			
			if key in self.template:
				
				#print(key, self.default_dict[key])
				if key in self.with_quote:
					self.template = re.sub(r"{0}{1}".format(key, regexp), '{0} "{1}"'.format(key, self.default_dict[key]), self.template, count=1 )
				elif key in self.with_brace:
					self.template = re.sub(r"{0}{1}".format(key, regexp2), key + " { " + self.default_dict[key] + "; ", self.template, count=0 )
				elif key in self.with_zone:	
					#print("trouve ?", re.search(r"{0}{1}[\t \w\d]*".format(regexp, key), self.template))
					self.template = re.sub(r"{0}{1}".format(key, regexp), "{0} {1}".format(key, self.default_dict[key]), self.template, count=1)
				else:
					self.template = re.sub(r"{0}{1}".format(key, regexp), "{0} {1}".format(key, self.default_dict[key]), self.template, count=1 )
					
				self.text_to_write = self.template	
			#print("\nkey = ", key, self.default_dict[key], self.text_to_write)	# a enlever, pour debuger
			
		ecrire_fichier(self.output_file, self.text_to_write)
		
		#print(self.text_to_write)	# pour le debogage, a supprimer

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
		self.output_file = "/home/administrateur/VDF_P6/resultat/dhcpd.conf"
		self.input_file = "/home/administrateur/VDF_P6/template/dhcpd.conf_tpl_debian"
		self.default_dict = { "domain-name": "exemple.org", \
		 "domain-name-servers": "8.8.8.8, 8.8.4.4", \
		  "default-lease-time": "600", \
		  "max-lease-time": "7200", \
		  "routers": "routeur1.exemple.org, routeur2.exemple.org", \
		  "authoritative": "#authoritative", \
		  "subnet": "172.16.100.0", \
  		  "range": "172.16.100.10 172.16.100.20", \
  		  "broadcast-address": "172.16.100.255" \
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
		#print("Le fichier {0} viens d'être créé sur le serveur".format(self.output_file))
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
		self.output_file = "/home/administrateur/VDF_P6/resultat/isc-dhcp-server"
		self.input_file = "/home/administrateur/VDF_P6/template/isc-dhcp-server_tpl_debian"
		self.default_dict = { "INTERFACES": "eth0"}
		self.entree = entree
		self.text_to_write = text_to_write
		try:
			if "INTERFACES" in self.entree.keys():
				self.text_to_write = 'INTERFACES="{0}"'.format(self.entree["INTERFACES"])
				#print(self.text_to_write)
				ecrire_fichier(self.output_file, self.text_to_write)
				#print("Le fichier {0} viens d'être créé sur le serveur".format(self.output_file))

			else:
				print("Pas trouvé la carte Interface dans le fichier ")
		except:
			print("erreur")

# LES FONCTIONS

# Définir la fonction ouverture du fichier yml ligne par ligne pour envoie à la fonction cleaning_yml
def ouverture_yml(monfichier):
	try:
		with open(monfichier, "r") as file_opened:
			return yaml.safe_load(file_opened)
	except IOError as exc:
		print("Le fichier : {0} n'est pas présent dans le disque.".format(exc.filename))
		error_texte = " Error 5 : Le fichier : {0} n'est pas présent dans le disque.\n".format(exc.filename)
		ecrire_error(log_file, error_texte)
	except yaml.YAMLError as exc:
		print(" Erreur d'ouverture du fichier yaml, vérifier qu'il s'agit d'un fichier YAML")
		print(exc)
		error_texte = " Error 5 : Erreur d'ouverture du fichier yaml, vérifier qu'il s'agit d'un fichier YAML.\n"
		ecrire_error(log_file, error_texte)
		


def ouverture(monfichier):
	""" ouverture des fichiers en mode ligne par ligne """
	try:
		with open(monfichier, "r") as file_opened:
			contenu = file_opened.read()
			return contenu
	except IOError as exc:
		print("Le fichier : {0} n'est pas présent dans le disque.".format(exc.filename))
		error_texte = " Error 5 : Le fichier : {0} n'est pas présent dans le disque.\n".format(exc.filename)
		ecrire_error(log_file, error_texte)

		
	except os.error as exc:
		print("Autre erreur", exc)



def ecrire_fichier(monfichier, contenu):
	# une fois le fichier template modifié, il est créé
	try:
		with open(monfichier, "w") as file_to_close:
			file_to_close.write(contenu)
	except:
		print("Erreur d'écriture du fichier {} ".format(monfichier))
		file_to_close.close()
		error_texte = " Error 5 : Erreur d'écriture du fichier {} \n".format(monfichier)
		ecrire_error(log_file, error_texte)

def ecrire_error(log_file, error_texte):
	try:
		now = time.strftime("%d %b %Y %H:%M")
		sys.exit(error_texte)
	except SystemExit:
		now += str(sys.exc_info()[1])
		print(now)
		with open(log_file, "a") as file_to_append:
			file_to_append.write(now)
	finally:
		sys.exit(0)


def ecrire_output(log_file, output_texte):
	now = time.strftime("%d %b %Y %H:%M")
	now += output_texte
	with open(log_file, "a") as file_to_append:
			file_to_append.write(now)
	


def connect_ssh(Vars_cnx, cmd, *cmd2):
	if Vars_cnx['connect']:
		IP_target = (Vars_cnx['connect']['IP_connexion'])
		user = (Vars_cnx['connect']['user_connexion'])
		output_texte = " La connexion au serveur {} c'est correctement effectuée.\n".format(IP_target)
		ecrire_output(log_file, output_texte)
	else:
		error_texte = " Error 6 : Problème de connexion ssh sur IP: {} \n".format(IP_target)
		ecrire_error(log_file, error_texte)

		

	lines =''
	ssh_client=paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
	# on lance la connexion avec le user et IP récupéré du dict Vars
	ssh_client.connect(hostname=IP_target, username=user)
	# onb execute la commande envoyé
	stdin, stdout, stderr = ssh_client.exec_command(cmd)
	# On renvoie le texte de la sortie standard et sortie erreur
	result_out = stdout.readlines()
	result_err = stderr.readlines()
	if result_out != []:
		lines += "SORTIE NORMALE :\n"
		for line in result_out:
			lines += line
	if result_err != []:		
		lines += "SORTIE ERREUR :\n"
		for line in result_err:
			lines += line
	# Si une deuxieme commande est appelée à être exécutée
	if cmd2:
		stdin, stdout, stderr = ssh_client.exec_command(cmd2[0])
		result_out = stdout.readlines()
		result_err = stderr.readlines()
		if result_out != []:
			lines += "SORTIE NORMALE :\n"
			for line in result_out:
				lines += line
		if result_err != []:		
			lines += "SORTIE ERREUR :\n"
			for line in result_err:
				lines += line
	ssh_client.close()		
	return(lines)
	
def copie_scp(Vars, source, destination):
	IP_target = (Vars['connect']['IP_connexion'])
	user = (Vars['connect']['user_connexion'])
	os.system("scp {0} {1}@{2}:{3}".format(source, user, IP_target, destination))


	



