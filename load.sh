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

# Vérifier les arguments
case "$1" in
    -adm)
        echo -e "\nAffichage des logs du conteneur : ecblflask..."
        docker-compose logs ecblflask
        ;;
    -?)
        echo -e "Usage: ./load.sh [-adm] [-?]"
        echo -e "Options:"
        echo -e "  -adm    Affiche les logs du conteneur ecblflask"
        echo -e "  -?      Affiche cette aide"
        ;;
    *)
        echo -e "\nAffichage des logs du conteneur : ecbldash..."
        docker-compose logs ecbldash
        ;;
esac