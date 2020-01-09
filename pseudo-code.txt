# **Pseudo Code for P6**


Lancer programme avec argument ( test, auto, semi-auto)
Si **auto** alors
   lancer *_ouverture_fichier*
   
Chercher adresse_IP dans le fichier (variable fixé a admin)
    Si adresse_IP trouvé alors:
        Connecter a la machine en ssh (clé déjà installé donc pas de mot de passe)
    sinon: 
        Exception 
        *ecrire_fichier_log* message Adresse IP non trouvé
    Test de réponse du serveur
        Si réponse alors:
            Chercher rôle dans fichier
                Si role trouvé alors:
                    lancer *installation_role*
                sinon:
                    exception
                    *ecrire_fichier_log* avec pas de rôle trouvé
        Sinon:
            exception
            *ecrire_fichier_log*
 

*OUVERTURE_FICHIER*
    ouvrir fichier yaml
    lire fichier yaml
    charger la liste dans une variable $donnee_yaml
    fermer le fichier
    
*INSTALLATION_ROLE*
    Role_name = role dans liste 
    $commande -install $role
    si exception:
        *ecrire_fichier_log* avec erreur d'installation
    sinon: 
        lancer *configuration_role*
        
*CONFIGURATION_ROLE*
    Lire $donnee_yaml en lien avec $role
    ecrire fichier $fichier_config_role suivant $role
    
    



*ECRIRE_FICHIER_LOG*
    récupérer message personnalisé et ecrire fichier /var/log/programme_ICS
