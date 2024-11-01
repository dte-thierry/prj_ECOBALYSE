#!/bin/bash

# Récupérer l'adresse IP publique de la VM
Public_IP=$(curl -s http://checkip.amazonaws.com)
Username=$(whoami)
SSH_Address="$Public_IP"

# Afficher le message d'accueil
echo -e "------------------------------------------"
echo -e "./load.sh : Accès au Framework Web Flask..."
echo -e "------------------------------------------"
echo -e "VM en cours, à l'adresse IP / SSH publique : $SSH_Address"

# Lancement de Flask 
echo -e "\nAffichage des logs du conteneur : ecblflask..."
docker-compose logs ecblflask
