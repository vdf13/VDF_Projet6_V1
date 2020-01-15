# -*- coding: utf-8 -*-
""" Programme principal d'installation et de configuration des rôles"""

#import os
from fonctions_RIAC import *


aa = "C:\\01_DATA\\PYTHON\\VDF_P6\\un_fichier.yml"
bb = "C:\\01_DATA\\PYTHON\\VDF_P6\\un_fichier2.yml"
cc = "C:\\01_DATA\\PYTHON\\VDF_P6\\autre_fichier.yml"
dd = "C:\\01_DATA\\PYTHON\\VDF_P6\\b_error_a_supprimer.yml" # erreur
ee = "C:\\01_DATA\\PYTHON\\VDF_P6\\template_dhcp.yml"
ff = "C:\\01_DATA\\PYTHON\\VDF_P6\\test_ecriture"

donnee = ouverture(aa)
template = ouverture(ee)
print(donnee)
print(template)
