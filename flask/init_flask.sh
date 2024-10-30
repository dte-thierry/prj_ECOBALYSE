#!/bin/bash

export FLASK_APP=test_flask.py
export FLASK_ENV=development

# Récupérer l'adresse IP publique de la VM
Public_IP=$(curl -s http://checkip.amazonaws.com)
Username=$(whoami)
SSH_Address="$Public_IP"

# Récupérer les constantes dans le conteneur
ECOBALYSE_VER=$(python3 /app/get_constants3.py ECOBALYSE_VER)
FLASK_LOG_NAMEFILE=$(python3 /app/get_constants3.py FLASK_LOG_NAMEFILE)

# Exporter la variable pour qu'elle soit accessible
export FLASK_LOG_NAMEFILE

# Afficher le message d'accueil
echo -e "--------------------------------------------------------------"
echo -e "ETAPE 03 : Consommation des Données Ecobalyse $ECOBALYSE_VER via Flask"
echo -e "--------------------------------------------------------------"
echo -e "VM utilisée, à l'adresse IP / SSH publique : $SSH_Address\n"


# Créer le répertoire logs s'il n'existe pas
mkdir -p logs

# Message
echo -e "Framework Web Flask démarré. Accessible depuis les adresses : 127.0.0.1:5000/ , ou : $SSH_Address:5000/"
echo -e "Fichier 'log' créé avec succès, par le conteneur.\n"

# Lancer Flask
flask run --host=0.0.0.0
