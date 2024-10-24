#!/bin/bash

# -----------------------------------------------------------------------------
# tips & tricks  
# -----------------------------------------------------------------------------

# Afficher la mémoire vive disponible
echo "Mémoire vive disponible : "
sudo free -h

# Forcer la suppression de tous les conteneurs, images, volumes, et réseaux inutilisés
echo "Suppression de tous les conteneurs inutilisés : " 
docker system prune -a --volumes -f

# Afficher l'espace disponible
echo "Espace disque maintenant disponible : "
df -h | egrep '(Filesystem|/dev/root)' | while read line; do
    echo -e "\t$line"
done
