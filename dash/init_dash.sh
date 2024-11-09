#!/bin/bash

export DASH_APP=test_dash.py
export DASH_ENV=development

# Récupérer l'adresse IP publique de la VM
Public_IP=$(curl -s http://checkip.amazonaws.com)
Username=$(whoami)
SSH_Address="$Public_IP"

# Récupérer les constantes dans le conteneur
ECOBALYSE_VER=$(python3 /app/get_constants4.py ECOBALYSE_VER)
DASH_LOG_NAMEFILE=$(python3 /app/get_constants4.py DASH_LOG_NAMEFILE)

# Exporter la variable pour qu'elle soit accessible
export DASH_LOG_NAMEFILE

# Afficher le message d'accueil
echo -e "--------------------------------------------------------------"
echo -e "ETAPE 03 : Consommation des Données Ecobalyse $ECOBALYSE_VER via Dash"
echo -e "--------------------------------------------------------------"
echo -e "VM utilisée, à l'adresse IP / SSH publique : $SSH_Address\n"


# Créer le répertoire logs s'il n'existe pas
mkdir -p logs

# Message
echo -e "Framework Web Dash démarré. Accessible depuis les adresses : 127.0.0.1:8050/ , ou : $SSH_Address:8050/"
echo -e "Fichier 'log' créé avec succès, par le conteneur.\n"

# Lancer Dash
python /app/test_dash.py
