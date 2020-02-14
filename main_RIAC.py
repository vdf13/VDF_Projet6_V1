#!/usr/bin/python2.7
#-*- coding: utf-8 -*-


#import os	

import sys, yaml
# import argparse,  paramiko
from new_fonctions import *
'''
option en utilisant les arguments

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dhcp", action="store_true", help="argument à utiliser pour dhcp")
parser.add_argument("-n", "--dns", action="store_true", help="argument à utiliser pour dns")
arg = parser.parse_args()

if arg.dhcp:
	role_arg = "dhcp"
if arg.dns:
	role_arg = "dns"
'''

log_file = "/home/administrateur/VDF_P6/resultat/riac.log"

# On teste qu'il y a bien le minimum d'argument dans la commande il en faut 3.
if len(sys.argv) <  3:
	print("précisez un fichier et une commande lors de l'execution du programme\nConnect\ninstall\nconfigure\ntest")
	error_texte = " Error 3: précisez un fichier et une commande lors de l'execution du programme\n"
	ecrire_error(log_file, error_texte)



# variables pour ouvrir le fichier yaml avec les arguments fichier et action
fichier_yml = sys.argv[1]	# nom du fichier en premier parametre
action = sys.argv[2]		# action qui sera effectué

# partie de sélection des actions en fonction de l'argument, apelle les fonctions ou classes
if action == "connect":
	print("Partie connexion lancé :")
	Vars_cnx = ouverture_yml(fichier_yml)
	
	# on lance la fonction connect_ssh qui utilise le module paramiko
	cmd = "ls /home/admin/dossier"
	cmd2 = "pwd"		# test a supprimer ainsi que cmd2 dans appel de fonction
	result = connect_ssh(Vars_cnx, cmd, cmd2)
	print(result)
	


elif action == "install":
	print("Partie installation lancé :")
	Vars_ins = ouverture_yml(fichier_yml)
	if Vars_ins['role_name']:
		if Vars_ins['role_name']['title'] == "dhcp":
			# installation dhcp
			package = "jshon"
			#os.system("ssh {0}@{1} 'touch fichier.TEST'; 'apt-get install {2}'; exit".format(user, IP_target, "isc-dhcp-server"))
			cmd = "sudo apt-get install {}".format(package)
			# commande qui servira à copier le fichier de config post install en .origin
			cmd2 = "cp /home/admin/fb /home/admin/fb.origin ; ls"
			# Commande pour vérifier le que la package a bien été installé
			cmd3 = "sudo apt list --installed {}*".format(package)
			result = connect_ssh(Vars_ins, cmd, cmd2, cmd3)
			#print(result)
			if package in result and "[installed]" in result:
				output_texte = " Le package {} viens d'être installé sur le serveur {} ".format(package, Vars_ins['connect']['IP_connexion'])
				ecrire_output(log_file, output_texte)
			# tester dans result la présence done et ecrire le log
			
		elif Vars_ins['role_name']['title'] == "dns":
			#installation dns
			package = "jshon"
			#os.system("ssh {0}@{1} 'touch fichier.TEST'; 'apt-get install {2}'; exit".format(user, IP_target, "bind9"))
			cmd = "sudo apt-get install {}".format(package)
			# commande qui servira à copier le fichier de config post install en .origin
			cmd2 = "cp /home/admin/fa /home/admin/fa.origin ; ls"
			# Commande pour vérifier le que la package a bien été installé
			cmd3 = "sudo apt list --installed {}*".format(package)
			result = connect_ssh(Vars_ins, cmd, cmd2, cmd3)
			print(result)
			if package in result and "[installed]" in result:
				output_texte = " Le package {} viens d'être installé sur le serveur {} ".format(package, Vars_ins['connect']['IP_connexion'])
				ecrire_output(log_file, output_texte)
			
		else:
			print("pas de role trouvé dans le fichier")
			# possibilité de rajouté un test sur la présence de title sinon erreur
			
			error_texte = " Error 4: Pas de role trouvé dans le fichier YAML\n"
			ecrire_error(log_file, error_texte)
			

elif action == "configure":
	# Actions qui seront effectuées pour la configuration dhcp ou dns
	Vars_cfg = ouverture_yml(fichier_yml)
	if Vars_cfg['role_name']:
		if Vars_cfg['role_name']['title'] == "dhcp":
			print("Partie configuration lancé : role = " + (Vars_cfg['role_name']['title']))
			# fichier dhcpd.conf
			dhcpd = DhcpdConf(Vars_cfg['role_name'])
			destination = "/home/admin/dossier/"
			copie_scp(Vars_cfg, dhcpd.output_file, destination, dhcpd.name_file)
			# fichier isc-dhcp-server
			isc = IscDhcpServer(Vars_cfg['role_name'])
			destination = "/home/admin/dossier/"	# un autre répertoire peut être défini
			copie_scp(Vars_cfg, isc.output_file, destination, isc.name_file)

			#result = connect_ssh(Vars_cfg, cmd)
			#print(result)

		elif Vars_cfg['role_name']['title'] == "dns":
			print("Partie configuration lancé : role = " + (Vars_cfg['role_name']['title']))
			# fichier 
			dns = Dns(Vars_cfg['role_name'])
			destination = "/home/admin/dossier/"
			copie_scp(Vars_cfg, dns.output_file, destination, dns.name_file)
			# fichier
			dns2 = Dns2(Vars_cfg['role_name2'])
			destination = "/home/admin/dossier/"
			copie_scp(Vars_cfg, dns2.output_file, destination, dns2.name_file)

		else:
			print("pas de role trouvé dans le fichier")
			# possibilité de rajouté un test sur la présence de title sinon erreur
			error_texte = " Error 4: Pas de role trouvé dans le fichier YAML\n"
			ecrire_error(log_file, error_texte)
			
	else:
		print("pas de role name dans le fichier YAML")
		error_texte = " Error 4: Pas de role trouvé dans le fichier YAML\n"
		ecrire_error(log_file, error_texte)

elif action == "test":
	print("Partie test lancé :")

elif action == "auto":
	print("Partie automatique lancé :")


else:
	print("L'action demandée est inconnue, la syntaxe est :\nprogramme.py fichier.yml [connect | install | configure | test | auto ]")
	error_texte = " Error 3: L'action demandée est inconnue\n"
	ecrire_error(log_file, error_texte)

