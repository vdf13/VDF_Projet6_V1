#!/usr/bin/python2.7
#-*- coding: utf-8 -*-


#import os	

import sys, yaml, time
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

# On teste qu'il y a bien le minimum d'argument dans la commande il en faut 3.
if len(sys.argv) <  3:
	print("précisez un fichier et une commande lors de l'execution du programme\nConnect\ninstall\nconfigure\ntest")
	sys.exit(0)


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
			#os.system("ssh {0}@{1} 'touch fichier.TEST'; 'apt-get install {2}'; exit".format(user, IP_target, "isc-dhcp-server"))
			cmd = "sudo apt-get install {}".format("jshon")
			# commande qui servira à copier le fichier de config post install en .origin
			cmd2 = "cp /home/admin/fb /home/admin/fb.origin ; ls"
			result = connect_ssh(Vars_ins, cmd, cmd2)
			print(result)
			
		elif Vars_ins['role_name']['title'] == "dns":
			#installation dns
			#os.system("ssh {0}@{1} 'touch fichier.TEST'; 'apt-get install {2}'; exit".format(user, IP_target, "bind9"))
			cmd = "sudo apt-get install {}".format("jshon")
			# commande qui servira à copier le fichier de config post install en .origin
			cmd2 = "cp /home/admin/fa /home/admin/fa.origin ; ls"
			result = connect_ssh(Vars_ins, cmd, cmd2)
			print(result)
			
		else:
			print("pas de role trouvé dans le fichier")
			# possibilité de rajouté un test sur la présence de title sinon erreur
			now = time.strftime("%d %b %Y %H:%M")
			print(now + " Inscrire erreur")
			sys.exit(0)

elif action == "configure":
	# Actions qui seront effectuées pour la configuration dhcp ou dns
	Vars_cfg = ouverture_yml(fichier_yml)
	if Vars_cfg['role_name']:
		if Vars_cfg['role_name']['title'] == "dhcp":
			print("Partie configuration lancé : role = " + (Vars_cfg['role_name']['title']))
			# fichier dhcpd.conf
			dhcpd = DhcpdConf(Vars_cfg['role_name'])
			destination = "/home/admin/dossier/"
			copie_scp(Vars_cfg, dhcpd.output_file, destination)
			# fichier isc-dhcp-server
			isc = IscDhcpServer(Vars_cfg['role_name'])
			destination = "/home/admin/dossier/"	# un autre répertoire peut être défini
			copie_scp(Vars_cfg, isc.output_file, destination)

			#result = connect_ssh(Vars_cfg, cmd)
			#print(result)

		elif Vars_cfg['role_name']['title'] == "dns":
			print("Partie configuration lancé : role = " + (Vars_cfg['role_name']['title']))
			# fichier 
			dns = Dns(Vars_cfg['role_name'])
			destination = "/home/admin/dossier/"
			copie_scp(Vars_cfg, dns.output_file, destination)
			# fichier
			dns2 = Dns2(Vars_cfg['role_name2'])
			destination = "/home/admin/dossier/"
			copie_scp(Vars_cfg, dns2.output_file, destination)

		else:
			print("pas de role trouvé dans le fichier")
			# possibilité de rajouté un test sur la présence de title sinon erreur
			now = time.strftime("%d %b %Y %H:%M")
			print(now + " Inscrire erreur")
			sys.exit(0)
	else:
		print("pas de role name dans le fichier")

elif action == "test":
	print("Partie test lancé :")

elif action == "auto":
	print("Partie automatique lancé :")

else:
	print("L'action demandée est inconnue, la syntaxe est :\nprogramme.py fichier.yml [connect | install | configure | test | auto ]")
	now = time.strftime("%d %b %Y %H:%M")
	print(now + " Inscrire erreur")
	sys.exit(0)


# création de l'objet dhcpd.conf
#dhcpd = DhcpdConf(val_yml)
#print("Le fichier {0} viens d'être créé avec les valeurs du fichier {1} .".format( dhcpd.output_file, file_yml))

'''
Mis en pause le temps de developper la partie connexion

fichier_yml = sys.argv[1]	# nom du fichier en premier parametre
info = sys.argv[2]			# title pour lire le nom du role à configurer


# ouverture du fichier source yaml et chargement des parametres dans le dictionnaire Vars
Vars = ouverture_yml(fichier_yml)
#print(Vars['role_name'])

if Vars['role_name'][info] == 'dhcp':
	print("Le rôle {0} va être configuré sur le serveur : {1}\n".format(Vars['role_name'][info], IP))
	dhcpd = DhcpdConf(Vars['role_name'])
	print("Le fichier {0} viens d'être créé avec les valeurs du fichier {1} .".format( dhcpd.output_file, fichier_yml))
	isc = IscDhcpServer(Vars['role_name'])
	print("Le fichier {0} viens d'être créé avec les valeurs du fichier {1} .".format( isc.output_file, fichier_yml))
elif Vars['role_name'][info] == 'dns':
	print("Le rôle {0} va être configuré sur le serveur : {1}\n".format(Vars['role_name'][info], IP))
	dns = Dns(Vars['role_name'])
	dns2 = Dns2(Vars['role_name2'])
	print("Le fichier {0} viens d'être créé avec les valeurs du fichier {1} .".format( dns.output_file, fichier_yml))
	print("Le fichier {0} viens d'être créé avec les valeurs du fichier {1} .".format( dns2.output_file, fichier_yml))
else:
	print("pas trouvé de role à installer")

'''

