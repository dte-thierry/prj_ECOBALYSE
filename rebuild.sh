#!/bin/bash

# Récupérer l'adresse IP publique de la VM
Public_IP=$(curl -s http://checkip.amazonaws.com)
Username=$(whoami)
SSH_Address="$Public_IP"

# Afficher le message d'accueil
echo -e "----------------------------------------------------------------"
echo -e "./rebuild.sh : (Re)Construction et (Re)démarrage des services..."
echo -e "----------------------------------------------------------------"
echo -e "VM en cours, à l'adresse IP / SSH publique : $SSH_Address"

# Reconstruire et redémarrer les services par 'docker-compose'
echo -e "\nArrête, reconstruit, et redémarre les services ..."
docker-compose down
docker-compose up -d --build