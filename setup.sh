#!/bin/bash

# Récupérer l'adresse IP publique de la VM
Public_IP=$(curl -s http://checkip.amazonaws.com)
Username=$(whoami)
SSH_Address="$Public_IP"

# Afficher le message d'accueil
echo -e "----------------------------------------------------------------"
echo -e "./setup.sh : (Re)Construction et (Re)démarrage des services..."
echo -e "----------------------------------------------------------------"
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

# Fonction pour reconstruire et redémarrer les services par 'docker-compose'
function docker_up {
    echo -e "\nArrête, reconstruit, et redémarre les services ..."
    docker-compose down
    docker-compose up -d --build
    # Afficher l'espace disque disponible
    echo -e "\nEspace disque disponible : "
    df -h | egrep '(Filesystem|/dev/root)' | while read line; do
        echo -e "\t$line"
    done


}

# Afficher le message d'utilisation
function usage {
    echo "Usage: $0 [-json]"
    exit 1
}

# Vérifier les arguments passés au script
case "$1" in
    -json)
        clear_logs
        clear_json
        docker_up
        ;;
    "")
        clear_logs
        docker_up
        ;;
    *)
        usage
        ;;
esac
