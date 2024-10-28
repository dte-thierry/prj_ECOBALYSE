#!/bin/bash

# Supprimer tous les fichiers .json dans le répertoire data
echo "Suppression de tous les fichiers .json dans le répertoire data"
sudo find ./data -type f -name "*.json" -exec rm -f {} \;

# Supprimer tous les fichiers .log dans le répertoire logs
echo "Suppression de tous les fichiers .log dans le répertoire logs"
find ./logs -type f -name "*.log" -exec rm -f {} \;
