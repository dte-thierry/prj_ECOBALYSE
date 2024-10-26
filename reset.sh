#!/bin/bash

# -----------------------------------------------------------------------------
# GitHub
# -----------------------------------------------------------------------------
# git clone https://github.com/dte-thierry/prj_ECOBALYSE.git


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

# activer la mémoire overcommit pour redis
echo "vm.overcommit_memory = 1" | sudo tee /etc/sysctl.conf
sudo sysctl "vm.overcommit_memory=1"
