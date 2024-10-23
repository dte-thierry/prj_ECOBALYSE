#!/bin/bash

# -----------------------------------------------------------------------------
# tips & tricks  
# -----------------------------------------------------------------------------

# Forcer la suppression de tous les conteneurs, images, volumes, et réseaux inutilisés
# echo "Suppression de tous les conteneurs inutilisés : " 
# docker system prune -a --volumes -f

# Afficher l'espace disponible
# echo "Espace disque maintenant disponible : "
# df -h | egrep '(Filesystem|/dev/root)' | while read line; do
#     echo -e "\t$line"
# done

# Afficher la mémoire vive disponible
# echo "Mémoire vive disponible : "
# sudo free -h

# construire l'image Docker en spécifiant le chemin du Dockerfile 
# echo "Construire l'image Docker de web_scraping : "
# docker build -f etl/Dockerfile -t ecbl-webscraping:extract .

# Lancer l'image Docker de web_scraping avec les répertoires /app/logs et /app/data montés en tant que volumes
# echo "Lancer l'image Docker de web_scraping : "
# docker run -v /home/ubuntu/prj_ECOBALYSE/logs:/app/logs -v /home/ubuntu/prj_ECOBALYSE/data:/app/data ecbl-webscraping:extract

# -----------------------------------------------------------------------------
# docker-compose 
# -----------------------------------------------------------------------------

# Reconstruire et redémarrer les services par 'docker-compose'
docker-compose up -d --build

# Arrêter les services
docker-compose down
