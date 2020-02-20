#!/usr/bin/python3.7
# -*- coding: utf-8 -*-

# Victor DE FARIA 2020-01-03 to 2020-02-18

import os, sys, paramiko
import re, yaml, time

# Chemin du fichier log du programme
log_file = "/home/administrateur/RIAC/riac.log"

# LES CLASSES des objets fichiers a créer
class Dns_zone:
	""" Classe qui va créer l'objet fichier db.zone
	Attributs de cette classe :
	- nom et chemin fichier entrée(template) et sortie(zone)
	- dictionnaire des valeurs par defaut si pas transmis en valeur entree, c'est le parametre par défaut qui est pris
	- méthodes : se créer, substituer texte
	"""

	def __init__(self, entree={}, text_to_write=''):
		# Création des attributs de l'objet 
		self.input_file = "/home/administrateur/RIAC/template/dns_zone_tpl_debian"
		self.output_file = "/home/administrateur/RIAC/resultat/db.test.dns"
		self.name_file = "db.test.dns"
		#self.time = time.strftime('%Y%m%d01')
		self.default_dict = {\
		'domain_name': 'serveur.exemple.org', \
		'domain_IP': '192.168.10.253', \
		'www_IP': '192.168.10.252', \
		'domain_email': 'webmaster.serveur.exemple.org', \
		'TTL': '604800', \
		'ORIGIN': 'exemple.org', \
		'serial': '2020020101', \
		'refresh': '3600', \
		'retry': '1200', \
		'expire': '2592000'\
		}
		self.default_dict['serial'] = time.strftime('%Y%m%d01')
		self.with_dollar = ('ORIGIN', 'TTL')
		self.with_SOA= ('serial', 'refresh', 'retry', 'expire')
		self.entree = entree
		self.template = ouverture(self.input_file)
		self.text_to_write = text_to_write
		# on remplace les valeurs des clés du dictionnaire défaut par les valeurs du fichier
		for key in self.entree.keys():
			if entree[key] == None:
				pass
			else:
				self.default_dict[key] = entree[key]

		# on apelle la fonction de remplacement du texte
		self.substitue()

	def substitue(self):
		'''
		Fonction qui remplace dans le texte template les valeur du dictionnaire par défaut modifé
		- fichier entrée yaml
		- dictionnaire par défaut
		'''
		# définitions des expressions régulières pour la substitution de texte
		regexp1 = '\$'				# pour partie qui commence par $
		regexp2 = '[\d\w]*\s;\s' 	# pour partie SOA
		
		for key in self.default_dict:
			# On teste toute les clés du dictionnaire pour les chercher dans le fichier template
			if key in self.template:
				# en fonction de la position du texte plusieurs types de séquence re remplacement 
				if key in self.with_dollar:
					self.template = re.sub(r"{0}{1}[\t \w\d]*".format(regexp1, key), '${0} {1}'.format(key, self.default_dict[key]), self.template, count=1 )
				elif key in self.with_SOA:
					self.template = re.sub(r"{0}{1}".format(regexp2, key), str(self.default_dict[key]) + " ; " + key, self.template, count=0 )
				else:
					self.template = re.sub(r"{0}".format(key), "{0}".format(self.default_dict[key]), self.template)	
				self.text_to_write = self.template	
			
		# Le résultat des modifications est envoyé à la fonction ecrire_fichier		
		ecrire_fichier(self.output_file, self.text_to_write)

class Dns_named:
	""" Classe qui va créer l'objet fichier named.conf
	Attributs de cette classe :
	- nom et chemin fichier entrée(template) et sortie(named.conf)
	- dictionnaire des valeurs par defaut si pas transmis en valeur entree, c'est le parametre par défaut qui est pris
	- méthodes : se créer, substituer texte
	"""

	def __init__(self, entree={}, text_to_write=''):
		# Création des attributs de l'objet 
		self.input_file = "/home/administrateur/RIAC/template/dns_named.conf_tpl_debian"
		self.output_file = "/home/administrateur/RIAC/resultat/named.conf"
		self.name_file = "named.conf"
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
		self.with_quote = ('directory', 'dump-file', 'statistics-file', 'zone')
		self.with_brace = ('forwarders', 'listen-on')
		self.with_zone = ('file')
		self.entree = entree
		self.template = ouverture(self.input_file)
		self.text_to_write = text_to_write

		# on remplace les valeurs des clés du dictionnaire défaut par les valeurs du fichier
		for key in self.entree.keys():
			if entree[key] == None:
				pass
			else:
				self.default_dict[key] = entree[key]

		# on apelle la fonction de remplacement du texte
		self.substitue()

	def substitue(self):
		'''
		Fonction qui remplace le texte du fichier template par les valeur du dictionnaire par défaut modifé
		- fichier entrée yaml
		- dictionnaire par défaut
		'''
		# définitions des expressions régulières pour la substitution de texte
		regexp1 = '[ ]"([\w".,-/]*)' # cas général avec texte entre ""  jusque trouver le ; 
		regexp2 = '[ ]{([\w .;]*)' # pour forwarders
		regexp3 = '[ ]([\w]*)' # pour type, remplcer texte sans les ""

		for key in self.default_dict:
			# On teste toute les clés du dictionnaire pour les chercher dans le fichier template
			if key in self.template:
				# en fonction de la position du texte plusieurs types de séquence re remplacement 
				if key in self.with_quote:
					self.template = re.sub(r"\b{0}{1}".format(key, regexp1), '{0} "{1}"'.format(key, self.default_dict[key]), self.template, count=1 )
				elif key in self.with_brace:
					self.template = re.sub(r"{0}{1}".format(key, regexp2), key + " { " + self.default_dict[key] + "; ", self.template, count=0 )
				elif key in self.with_zone:	
					self.template = re.sub(r" {0}{1}".format(key, regexp1), ' {0} "{1}"'.format(key, self.default_dict[key]), self.template, count=1)	
				else:
					self.template = re.sub(r"{0}{1}".format(key, regexp3), '{0} {1}'.format(key, self.default_dict[key]), self.template, count=1 )
				self.text_to_write = self.template	
			
		# Le résultat des modifications est envoyé à la fonction ecrire_fichier	
		ecrire_fichier(self.output_file, self.text_to_write)


class DhcpdConf:
	""" Classe qui va créer l'objet fichier dhcpd.conf
	Attributs de cette classe :
	- nom fichier entrée et sortie
	- dictionnaire des valeurs par defaut si pas transmis en valeur entree, c'est le parametre par défaut qui est pris
	- méthodes : se créer, substituer texte
	"""

	def __init__(self, entree={}, text_to_write=''):
		# Création des attributs de l'objet 
		self.input_file = "/home/administrateur/RIAC/template/dhcpd.conf_tpl_debian"
		self.output_file = "/home/administrateur/RIAC/resultat/dhcpd.conf"
		self.name_file = "dhcpd.conf"
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
		self.template = ouverture(self.input_file)
		self.entree = entree
		self.text_to_write = text_to_write
		
		# on remplace les valeurs des clés du dictionnaire défaut par les valeurs du fichier
		for key in self.entree.keys():
			if entree[key] == None:
				pass
			else:
				self.default_dict[key] = entree[key]
		# on apelle la fonction de remplacement du texte
		self.substitue()
		
	def substitue(self):
		'''
		Fonction qui remplace dans le texte template les valeur du dictionnaire par défaut modifé
		- fichier entrée yaml
		- dictionnaire par défaut
		'''
		# définitions des expressions régulières pour la substitution de texte
		regexp = '[ ]([\w"., -]*)' # key+_.," en fait jusque trouver le ;
		

		for key in self.default_dict:
			# On teste toute les clés du dictionnaire pour les chercher dans le fichier template
			self.template = re.sub(r"{0}{1}".format(key, regexp), "{0} {1}".format(key, self.default_dict[key]), self.template)
			self.text_to_write = self.template
		
		# Le résultat des modifications est envoyé à la fonction ecrire_fichier		
		ecrire_fichier(self.output_file, self.text_to_write)

class IscDhcpServer:
	""" Class qui va créer le fichier isc-dhcp-server avec la carte interface
	Attributs de cette classe :
	- nom fichier entrée et sortie
	- dictionnaire des valeurs par defaut si pas transmis en valeur entree, c'est le parametre par défaut qui est pris
	- méthodes : se créer
	"""
	def __init__(self, entree={}, text_to_write=''):
		self.input_file = "/home/administrateur/RIAC/template/isc-dhcp-server_tpl_debian"
		self.output_file = "/home/administrateur/RIAC/resultat/isc-dhcp-server"
		self.name_file = "isc-dhcp-server"
		self.default_dict = { "INTERFACES": "eth0"}
		self.entree = entree
		self.text_to_write = text_to_write
		try:
			if "INTERFACES" in self.entree.keys():
				self.text_to_write = 'INTERFACES="{0}"'.format(self.entree["INTERFACES"])

				# Le résultat est envoyé à la fonction ecrire_fichier
				ecrire_fichier(self.output_file, self.text_to_write)
			else:
				print("Pas trouvé la carte Interface dans le fichier ")
				# inserer un code erreur et log
		except:
			print("erreur")
			# inserer un code erreur et log

# LES FONCTIONS
 
def ouverture_yml(monfichier):
	''' Fonction d'ouverture du fichier yml pour le dictionnaire self.template des classes
	gestion des erreurs d'ouverture de fichiers et appele ecrire_error en cas d'erreur
	'''
	try:
		# On ouvre le fichier et on vérifie que l'on charge un dictionnaire, sinon erreur généré
		with open(monfichier, "r") as file_opened:
			contenu = yaml.safe_load(file_opened)
			if type(contenu) is dict:
				return contenu
			else:
				error_texte = " Error 3 : Erreur d'ouverture du fichier {}, vérifier qu'il s'agit d'un fichier YAML correctement rempli.\n".format(monfichier)
				ecrire_error(log_file, error_texte)

	except IOError as exc:
		print("Le fichier : {0} n'est pas présent dans le disque.".format(exc.filename))
		error_texte = " Error 3 : Le fichier : {0} n'est pas présent dans le disque.\n".format(exc.filename)
		ecrire_error(log_file, error_texte)
	except yaml.YAMLError as exc:
		print(" Erreur d'ouverture du fichier yaml, vérifier qu'il s'agit d'un fichier YAML")
		print(exc)
		error_texte = " Error 3 : Erreur d'ouverture du fichier yaml, vérifier qu'il s'agit d'un fichier YAML.\n"
		ecrire_error(log_file, error_texte)
	
def ouverture(monfichier):
	""" ouverture des fichiers en mode ligne par ligne """
	try:
		with open(monfichier, "r") as file_opened:
			contenu = file_opened.read()
			return contenu
	except IOError as exc:
		print("Le fichier : {0} n'est pas présent dans le disque.".format(exc.filename))
		error_texte = " Error 3 : Le fichier : {0} n'est pas présent dans le disque.\n".format(exc.filename)
		ecrire_error(log_file, error_texte)	
	except os.error as exc:
		error_texte = " Error 3 : Une erreur : {0} lors de l'ouverture du fichier. Vérifier le fichier.\n".format(exc.filename)
		ecrire_error(log_file, error_texte)	
		

def ecrire_fichier(monfichier, contenu):
	''' Fonction d'écriture dans le fichier souhaité du texte modifié
	Gestion des erreurs appele ecrire_error si besoin
	'''

	try:
		with open(monfichier, "w") as file_to_close:
			file_to_close.write(contenu)
	except:
		print("Erreur d'écriture du fichier {} ".format(monfichier))
		file_to_close.close()
		error_texte = " Error 4 : Erreur d'écriture du fichier {} \n".format(monfichier)
		ecrire_error(log_file, error_texte)


def ecrire_error(log_file, error_texte):
	''' Fonction d'écriture dans le fichier log en cas d'erreur
	Ajoute la date au texte envoyé à la fonction
	'''
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
	''' Fonction d'écriture dans le fichier log en cas de création normale du fichier
	Ajoute la date au texte envoyé à la fonction
	'''
	now = time.strftime("%d %b %Y %H:%M")
	now += output_texte
	with open(log_file, "a") as file_to_append:
			file_to_append.write(now)
	


def connect_ssh(Vars_cnx, *cmd):
	''' Fonction de connexion ssh et exécution de la commande envoyé en argument
	Gestion des erreurs et appele ecrire_error si besoin ou ecrire_output en cas de réussite
	'''
	lines =''
	ssh_client=paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
	if Vars_cnx['connect']:
		IP_target = (Vars_cnx['connect']['IP_connexion'])
		user = (Vars_cnx['connect']['user_connexion'])
		# on teste la connexion au serveur et leve une erreur si connexion impossible
		try:
			ssh_client.connect(hostname=IP_target, username=user)
			# on execute la ou les commandes envoyés en argument
			if cmd:
				for cmdi in cmd:
					stdin, stdout, stderr = ssh_client.exec_command(cmdi)
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
			
			output_texte = " La connexion au serveur {} c'est correctement effectuée.\n".format(IP_target)
			ecrire_output(log_file, output_texte)	
			# On cloture la connexion ssh et on renvoie les lignes capturées par stdout et stderr
			ssh_client.close()		
			return(lines)
		except:
			error_texte = " Error 4 : Problème de connexion ssh sur le serveur: {} \n".format(IP_target)
			ecrire_error(log_file, error_texte)	
	else:
		error_texte = " Error 5 : Le fichier ne contient pas de valeurs pour la connexion ssh sur IP:\n"
		ecrire_error(log_file, error_texte)

def copie_scp(Vars, source, destination, name_file):
	''' Fonction de copie du fichier créé par les classes dans le répertoire du serveur
	Gestion des erreurs et appele ecrire_error si besoin ou ecrire_output en cas de réussite
	'''
	IP_target = (Vars['connect']['IP_connexion'])
	user = (Vars['connect']['user_connexion'])
	os.system("scp {0} {1}@{2}:{3}".format(source, user, IP_target, destination))
	output_texte = " Le fichier {0}{1} à été configuré sur le serveur {2} .\n".format(destination, name_file, IP_target)
	ecrire_output(log_file, output_texte)
	# Ajouter une gestion d'erreur 





