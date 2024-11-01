#!/bin/bash

# Récupérer l'adresse IP publique de la VM
Public_IP=$(curl -s http://checkip.amazonaws.com)
Username=$(whoami)
SSH_Address="$Public_IP"

# Afficher le message d'accueil
echo -e "------------------------------------------------------"
echo -e "./init.sh : (Ré)Initialisation du projet Ecobalyse..."
echo -e "------------------------------------------------------"
echo -e "VM en cours, à l'adresse IP / SSH publique : $SSH_Address"

# activer la mémoire overcommit pour redis
echo "vm.overcommit_memory = 1" | sudo tee /etc/sysctl.conf
sudo sysctl "vm.overcommit_memory=1" || true 

# Forcer la suppression de tous les conteneurs, images, volumes, et réseaux inutilisés
echo "Suppression de tous les conteneurs inutilisés : " 
docker system prune -a --volumes -f

# Supprimer les anciennes données Redis
echo "Suppression des anciennes données Redis"
sudo rm -rf ./data/redis/*

# Supprimer les anciennes données MongoDB
echo "Suppression des anciennes données MongoDB"
sudo rm -rf ./data/mongo/*

# Supprimer tous les fichiers .json dans le répertoire data
echo "Suppression de tous les fichiers .json dans le répertoire data"
sudo find ./data -type f -name "*.json" -exec rm -f {} \;

# Supprimer tous les fichiers .log dans le répertoire logs
echo "Suppression de tous les fichiers .log dans le répertoire logs"
find ./logs -type f -name "*.log" -exec rm -f {} \;

# Afficher la mémoire vive disponible
echo "Mémoire vive disponible : "
sudo free -h

# Afficher l'espace disponible
echo "Espace disque maintenant disponible : "
df -h | egrep '(Filesystem|/dev/root)' | while read line; do
    echo -e "\t$line"
done
