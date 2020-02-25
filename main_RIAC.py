#!/usr/bin/python3.7
#-*- coding: utf-8 -*-
# Victor DE FARIA 2020-01-03 to 2020-02-18

import sys, yaml
from fonctions_RIAC import *

#log_file = "/home/administrateur/VDF_P6/resultat/riac.log"
log_file = "/home/administrateur/RIAC/riac.log"


# DEFINITIONS DES FONCTIONS
def connect():
	print("Partie connexion lancé :")
	Vars_cnx = ouverture_yml(fichier_yml)
	
	# on lance la fonction connect_ssh qui utilise le module paramiko
	cmd = "ls $HOME"
	result = connect_ssh(Vars_cnx, cmd)
	if action == "connect":
		print("La connexion au serveur s'est effectué correctement et la commande 'ls' executé sur le répertoire de l'utilisateur:\n{}".format(result))

def install():
	Vars_ins = ouverture_yml(fichier_yml)
	if Vars_ins['role_name']:
		# Installation  dhcp
		if Vars_ins['role_name']['title'] == "dhcp":
			print("Partie installation lancé : role = " + (Vars_ins['role_name']['title']))
			# installation du service dhcp
			package = "isc-dhcp-server"
			# commande pour l'installation du package
			cmd = "sudo apt-get install -y {}".format(package)
			# commande qui servira à copier le fichier de config post install en .origin
			cmd2 = "sudo cp /etc/dhcp/dhcpd.conf /etc/dhcp/dhcpd.conf.origin ; ls"
			# Commande pour vérifier le que le package a bien été installé
			cmd3 = "sudo apt list --installed {}*".format(package)
			result = connect_ssh(Vars_ins, cmd, cmd2, cmd3)
			#print(result)	pour debugage
			if package in result and "[installed]" in result:
				output_texte = " Le package {} viens d'être installé sur le serveur {} ".format(package, Vars_ins['connect']['IP_connexion'])
				ecrire_output(log_file, output_texte)
			else:
				output_texte = " Error 6 : Le package {} n'a pas été trouvé sur le serveur {} ".format(package, Vars_ins['connect']['IP_connexion'])
				ecrire_error(log_file, output_texte)
		# Installation dns
		elif Vars_ins['role_name']['title'] == "dns":
			print("Partie installation lancé : role = " + (Vars_ins['role_name']['title']))
			#installation du service dns
			package = "bind9"
			# commande pour l'installation du package
			cmd = "sudo apt-get install -y {}".format(package)
			# commande qui servira à copier le fichier de config post install en .origin
			cmd2 = "sudo cp /etc/bind/named.conf /etc/bind/named.conf.origin ; ls"
			# Commande pour vérifier le que la package a bien été installé
			cmd3 = "sudo apt list --installed {}*".format(package)
			result = connect_ssh(Vars_ins, cmd, cmd2, cmd3)
			#print(result)		pour debugage
			if package in result and "[installed]" in result:
				output_texte = " Le package {} viens d'être installé sur le serveur {} ".format(package, Vars_ins['connect']['IP_connexion'])
				ecrire_output(log_file, output_texte)
			else:
				output_texte = " Error 6 : Le package {} n'a pas été trouvé sur le serveur {} ".format(package, Vars_ins['connect']['IP_connexion'])
				ecrire_error(log_file, output_texte)
		else:
			error_texte = " Error 5: Le role : {} trouvé dans le fichier YAML n'est pas correct.\nUsage title:[ dns | dhcp ]\n".format(Vars_ins['role_name']['title'])
			ecrire_error(log_file, error_texte)

def configure():
	# Actions qui seront effectuées pour la configuration dhcp ou dns
	Vars_cfg = ouverture_yml(fichier_yml)
	if Vars_cfg['role_name']:
		# Configuration dhcp
		if Vars_cfg['role_name']['title'] == "dhcp":
			print("Partie configuration lancé : role = " + (Vars_cfg['role_name']['title']))
			# création de l'objet fichier dhcpd.conf
			dhcpd = DhcpdConf(Vars_cfg['part_dhcp_conf'])
			destination = "/tmp/"
			#destination = "/etc/dhcp/"
			print("Partie copie des fichier sur le serveur :")
			copie_scp(Vars_cfg, dhcpd.output_file, destination, dhcpd.name_file)
			# création de l'objet fichier isc-dhcp-server
			isc = IscDhcpServer(Vars_cfg['part_dhcp_interface'])
			destination = "/tmp/"	# un autre répertoire peut être défini
			#destination = "/etc/default/"
			copie_scp(Vars_cfg, isc.output_file, destination, isc.name_file)

			# commande qui servira à copier le fichier de config post install en .origin
			cmd1 = "sudo cp /tmp/dhcpd.conf /etc/dhcp/dhcpd.conf"
			cmd2 = "sudo cp /tmp/isc-dhcp-server /etc/default/isc-dhcp-server"
			#destination = "/etc/dhcp/"
			#destination = "/etc/default/"
			result = connect_ssh(Vars_cfg, cmd1, cmd2)
			if 'ERREUR' in result:
				error_texte = " Error 4 : Erreur lors de la copie des fichiers : {0} {1}".format(dhcpd.name_file, isc.name_file)
				ecrire_error(log_file, error_texte)
				
		# Configuration dns
		elif Vars_cfg['role_name']['title'] == "dns":
			print("Partie configuration lancé : role = " + (Vars_cfg['role_name']['title']))
			# création de l'objet fichier named.conf
			dns_named = Dns_named(Vars_cfg['part_dns_named'])
			destination = "/tmp/"
			copie_scp(Vars_cfg, dns_named.output_file, destination, dns_named.name_file)

			cmd = "sudo cp /tmp/named.conf /etc/bind/named.conf"
			result = connect_ssh(Vars_cfg, cmd)

			if 'ERREUR' in result:
				error_texte = " Error 4 : Erreur lors de la copie du fichier : {}".format(dns_named.name_file)
				ecrire_error(log_file, error_texte)

			# création de l'objet fichier zone
			dns_zone = Dns_zone(Vars_cfg['part_dns_zone'])
			destination = "/tmp/"
			copie_scp(Vars_cfg, dns_zone.output_file, destination, dns_zone.name_file)
			cmd = "sudo cp /tmp/{0} /etc/bind/{0}".format(dns_zone.name_file)
			result = connect_ssh(Vars_cfg, cmd)
			if 'ERREUR' in result:
				error_texte = " Error 4 : Erreur lors de la copie du fichier : {}".format(dns_zone.name_file)
				ecrire_error(log_file, error_texte)
		else:
			error_texte = " Error 5: Le role : {} trouvé dans le fichier YAML n'est pas correct.\nUsage title:[ dns | dhcp ]\n".format(Vars_cfg['role_name']['title'])
			ecrire_error(log_file, error_texte)	
	else:
		print("pas de role name dans le fichier YAML")
		error_texte = " Error 5 : Pas de role name dans le fichier YAML "
		ecrire_error(log_file, error_texte)
	
def test():
	''' Fonction qui vérifie la présence des éléments indispensables dans le fichier YAML
	role_name, title, connect
	'''
	Vars_tst = ouverture_yml(fichier_yml)
	if 'role_name' in Vars_tst:
		if 'title' in Vars_tst['role_name']:
			if 'connect' in Vars_tst:
				return
			else:
				error_texte = " Error 5: Vérifier la syntaxe  dans le fichier YAML\nPartie 'connect'"
				ecrire_error(log_file, error_texte)
		else:
			error_texte = " Error 5: Vérifier la syntaxe  dans le fichier YAML\nPartie 'title'"
			ecrire_error(log_file, error_texte)
	else:
		error_texte = " Error 5: Vérifier la syntaxe  dans le fichier YAML\nPartie 'role_name'"
		ecrire_error(log_file, error_texte)

		
# ////////////////////////////// CODE PRINCIPAL //////////////////////

# On teste qu'il y a bien le minimum d'argument dans la commande il en faut 3.
if len(sys.argv) <  3:
	print("précisez un fichier et une commande lors de l'execution du programme\nConnect\ninstall\nconfigure")
	error_texte = " Error 2: précisez un fichier et une commande lors de l'execution du programme\n"
	ecrire_error(log_file, error_texte)

# variables pour ouvrir le fichier yaml avec les arguments fichier et action
fichier_yml = sys.argv[1]	# nom du fichier en premier parametre
action = sys.argv[2]		# action qui sera effectué


# partie de sélection des actions en fonction de l'argument, apelle les fonctions ou classes
if action =="test":
	test()
elif action == "connect":
	test()
	connect()
elif action == "install":
	test()
	install()
elif action == "configure":
	test()
	configure()
elif action == "auto":
	# Actions qui seront effectuées automatiquement pour la configuration dhcp ou dns
	test()
	connect()
	install()
	configure()

else:
	print("L'action demandée est inconnue, la syntaxe est :\npython programme.py fichier.yml [connect | install | configure | auto ]")
	error_texte = " Error 2: L'action demandée est inconnue.\nUsage : python programme.py fichier.yml [connect | install | configure | auto ]"
	ecrire_error(log_file, error_texte)

print("Programme RIAC correctement terminé. Fonction : {}".format(action))
output_texte = " Programme RIAC correctement terminé. Fonction : {}".format(action)
ecrire_output(log_file, output_texte)
