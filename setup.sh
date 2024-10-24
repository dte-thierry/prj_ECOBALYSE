#!/bin/bash

# -----------------------------------------------------------------------------
# Dockerfile  
# -----------------------------------------------------------------------------

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
# docker-compose up -d --build
docker-compose up --build

# Arrêter les services
docker-compose down
