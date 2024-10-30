#!/bin/bash

# Fonction pour afficher la version de Docker
function show_version {
    echo -e "\nVérification de la version de Docker..."
    docker --version
}

# Fonction pour afficher les conteneurs Docker en cours d'exécution
function show_containers {
    echo -e "\nListe des conteneurs Docker en cours d'exécution..."
    docker ps
}

# Fonction pour afficher les logs des conteneurs
function show_logs {
    echo -e "\nAffichage des logs du conteneur : ecblwebscraping..."
    docker-compose logs ecblwebscraping
    echo -e "\nAffichage des logs du conteneur : ecblmongodb..."
    docker-compose logs ecblmongodb
    echo -e "\nAffichage des logs du conteneur : ecblredis..."
    docker-compose logs ecblredis
}

# Fonction pour afficher les images Docker disponibles
function show_images {
    echo -e "\nListe des images Docker disponibles..."
    docker images

    # Calcul de la taille totale des images Docker
    total_size=0
    while read -r size unit; do
        if [ "$unit" == "GB" ]; then
            total_size=$(echo "$total_size + $size" | bc)
        elif [ "$unit" == "MB" ]; then
            size_in_gb=$(echo "scale=2; $size / 1024" | bc)
            total_size=$(echo "$total_size + $size_in_gb" | bc)
        fi
    done < <(docker images --format "{{.Size}}" | sed 's/ //g' | sed 's/GB/ GB/g' | sed 's/MB/ MB/g' | awk '{print $1, $2}')

    # echo -e "\nLa taille totale des images Docker est de ${total_size} GB.\n"
}

# Fonction pour afficher toutes les informations
function show_all {
    show_version
    show_containers
    show_images
    show_logs
}

# Récupérer l'adresse IP publique de la VM
Public_IP=$(curl -s http://checkip.amazonaws.com)
Username=$(whoami)
SSH_Address="$Public_IP"

# Afficher le message d'accueil
echo -e "-----------------------------------------------------"
echo -e "./info.sh : Informations sur les conteneurs Docker..."
echo -e "-----------------------------------------------------"
echo -e "VM en cours, à l'adresse IP / SSH publique : $SSH_Address"

# Analyser les options de ligne de commande
if [ "$1" == "-all" ]; then
    show_all
    exit 0
fi

if [ "$1" == "-logs" ]; then
    show_logs
    exit 0
fi

while getopts "vai" opt; do
    case $opt in
        v)
            show_version
            exit 0
            ;;
        a)
            show_containers
            exit 0
            ;;
        i)
            show_images
            exit 0
            ;;
        *)
            echo "Usage: $0 [-v] [-a] [-i] [-all] [-logs]"
            exit 1
            ;;
    esac
done

# Si aucune option valide n'est fournie
echo "Usage: $0 [-v] [-a] [-i] [-all] [-logs]"
exit 1