#!/bin/bash

echo -e "\nVérification de la version de Docker..."
docker --version

echo -e "\nListe des conteneurs Docker en cours d'exécution..."
docker ps

echo -e "\nInformations sur Docker..."
docker info

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

echo -e "\nLa taille totale des images Docker est de ${total_size} GB.\n"