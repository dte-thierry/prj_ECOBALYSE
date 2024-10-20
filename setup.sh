#!/bin/bash

# Arrêter et supprimer les conteneurs existants, mais conserver les volumes
docker-compose down --volumes

# Construire les images Docker et lancer les conteneurs
docker-compose up -d --build