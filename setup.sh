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

# Reconstruire et redémarrer les services par 'docker-compose'
# docker-compose up --build
docker-compose up -d --build
