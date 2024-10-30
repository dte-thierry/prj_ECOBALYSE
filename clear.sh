#!/bin/bash

# Récupérer l'adresse IP publique de la VM
Public_IP=$(curl -s http://checkip.amazonaws.com)
Username=$(whoami)
SSH_Address="$Public_IP"

# Afficher le message d'accueil
echo -e "-----------------------------------------------"
echo -e "./clear.sh : Nettoyage des données Ecobalyse..."
echo -e "-----------------------------------------------"
echo -e "VM en cours, à l'adresse IP / SSH publique : $SSH_Address"

# Fonction pour supprimer les fichiers JSON
function clear_json {
    echo "Suppression de tous les fichiers .json dans le répertoire data"
    sudo find ./data -type f -name "*.json" -exec rm -f {} \;
}

# Fonction pour supprimer les fichiers de logs
function clear_logs {
    echo "Suppression de tous les fichiers .log dans le répertoire logs"
    find ./logs -type f -name "*.log" -exec rm -f {} \;
}

# Fonction pour tout supprimer
function clear_all {
    clear_json
    clear_logs
}

# Analyser les options de ligne de commande
case "$1" in
    -logs)
        clear_logs
        ;;
    -json)
        clear_json
        ;;
    -all|"")
        clear_all
        ;;
    *)
        echo "Usage: $0 [-logs] [-json] [-all]"
        exit 1
        ;;
esac