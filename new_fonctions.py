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
	- liste des clés de l'objet = local_keys   la conversion de valeurs ne se fait que sur les clés de cette liste
	- méthodes : se créer,  écrire texte, substituer texte de input_file
	
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
		 # enlever cette partie , ne sers plus !
		'''
		self.local_keys = ["domain-name", \
		 "domain-name-servers", \
		 "default-lease-time", \
		 "max-lease-time", \
		 "authoritative" \
		 ]  
		'''
		self.text_to_write = text_to_write
		self.lines = ouverture(self.input_file)
		# pour utiliser le module re texte chargé en intégralité
		self.lines_re = ouverture_re(self.input_file)
		# c'est le dictionnaire Vars qui est chargé en entree
		
		self.entree = entree
		
		# symbole a ajouter pour finir la ligne
		self.end_line = ";\n"


		
		# on remplace le dictionnaire par défaut par les valeurs chargées //// Poursuivre
		for key in self.entree.keys():
			self.default_dict[key] = entree[key]
		print("default dict après = ", self.default_dict)

		# on lance le modue qui utilise re
		self.resub()
			
		# on apelle la fonction de remplacement du texte
		#self.substitue()
	# création auutre méthode substitue avec utilisation des expressions régulières
	def resub(self):
		''' 
		méthode pour substituer le texte par les valeurs du dictionnaire modifié
		utilse le module re pour les expressions régulières

		'''
		texte = ' \nUne phrase avec domain-name et range qui.peut.se.trouver et netmask dans; fichier source \n\
option domain-name "example.org";\n\
option domain-name-servers ns1.example.org, ns2.example.org;\n\
default-lease-time 600;\n\
max-lease-time 7200;\n\
subnet 10.254.239.0 netmask 255.255.255.224 {\n\
  range 10.254.239.10 10.254.239.20;\n\
  option routers rtr-239-0-1.example.org, rtr-239-0-2.example.org;\
}\n'

		print(texte)


		exp = "([ ]+\w*)"	# fonctionne pour un espace + mot sans symbole
		exp1 = '([ ]+[\w".,]*)'	# fonctionne pour espace + mot avec alpha + " . enlève tout jusque la , ;
		
		for key in self.default_dict:
			#print(key)
			#if key in self.lines_re:
			if key in texte:
				#re.sub(r"{0}".format(key), "toto", self.lines_re)
				texte = re.sub(r"{0}{1}*".format(key, exp1), "{0} {1}".format(key, self.default_dict[key]), texte)
				#print("Trouvé ")
				

		print(texte)
	
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
				for val in list(self.default_dict):
					if val in line:
						cc = line.find(val, 0, len(line))
						texte += line[:cc] + str(val) + " " + str(self.default_dict[val])+ self.end_line
						break # Important pour finir la condition
				else:
					texte += line + "\n"

		self.text_to_write = texte
		ecrire_fichier(self.output_file, self.text_to_write)






# LES FONCTIONS

# Définir la fonction ouverture du fichier yml ligne par ligne pour envoie à la fonction cleaning_yml
def ouverture_yml(monfichier):
	with open(monfichier, "r") as file_opened:
		try:
			return yaml.safe_load(file_opened)
		except yaml.YAMLError as exc:
			print(exc)

def ouverture_re(monfichier):
	""" ouverture des fichiers en mode ligne par ligne """
	# voir si pas doublon avec le fonction ouverture_yml qui est aussi en mode ligne
	try:
		with open(monfichier, "r") as file_opened:
			contenu = file_opened.read()
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



