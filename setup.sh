#!/bin/bash

# -----------------------------------------------------------------------------
# docker
# -----------------------------------------------------------------------------

# construire l'image Docker en spécifiant le chemin du Dockerfile 
# echo "Construire l'image Docker de web_scraping : "
# docker build -f etl/Dockerfile -t ecbl-webscraping:extract .

# Lancer l'image Docker de web_scraping avec les répertoires /app/logs et /app/data montés en tant que volumes
# echo "Lancer l'image Docker de web_scraping : "
# docker run -v /home/ubuntu/prj_ECOBALYSE/logs:/app/logs -v /home/ubuntu/prj_ECOBALYSE/data:/app/data ecbl-webscraping:extract

# -----------------------------------------------------------------------------
# redis 
# -----------------------------------------------------------------------------
# vérifier les logs pour voir la sortie de test_redis.py
# docker-compose logs redis 

# -----------------------------------------------------------------------------
# docker-compose 
# -----------------------------------------------------------------------------

# afficher les services Docker et vérifier leur état
# docker-compose ps


# Récupérer l'adresse IP publique de la VM
Public_IP=$(curl -s http://checkip.amazonaws.com)
Username=$(whoami)
SSH_Address="$Public_IP"

# Afficher le message d'accueil
echo -e "--------------------------------------------------------------------"
echo -e "./setup.sh : (Re)Configuration et Lancement des conteneurs Docker..."
echo -e "--------------------------------------------------------------------"
echo -e "VM en cours, à l'adresse IP / SSH publique : $SSH_Address"

# Reconstruire et redémarrer les services par 'docker-compose'
# docker-compose up --build
docker-compose up -d --build
