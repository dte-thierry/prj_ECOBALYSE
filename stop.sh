#!/bin/bash

# -----------------------------------------------------------------------------
# docker-compose 
# -----------------------------------------------------------------------------

# Récupérer l'adresse IP publique de la VM
Public_IP=$(curl -s http://checkip.amazonaws.com)
Username=$(whoami)
SSH_Address="$Public_IP"

# Afficher le message d'accueil
echo -e "----------------------------------------"
echo -e "./stop.sh : Arrêt des services Docker..."
echo -e "----------------------------------------"
echo -e "VM en cours, à l'adresse IP / SSH publique : $SSH_Address"

# arrête tous les conteneurs définis dans le fichier docker-compose.yml
docker-compose down