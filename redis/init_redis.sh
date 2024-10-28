#!/bin/bash

# Créer le répertoire logs s'il n'existe pas
mkdir -p /app/logs

# Démarrer Redis en arrière-plan
redis-server /usr/local/etc/redis/redis.conf &

# Attendre que Redis soit prêt
sleep 5

# Attendre que le fichier JSON soit créé
echo -e "\nTest Redis de récupération JSON : "
echo -e "Attendre que le fichier JSON soit créé...\n"
while [ ! -f /app/data/PRJ-ECOBALYSE-01-WEB_SCRAPING1_temp1.json ]; do
  sleep 8
done

# Exécuter le script de test
/opt/venv/bin/python /app/test_redis.py &> /app/logs/docker_testredis_$(date +"%Y-%m-%d_%H-%M-%S").log

# Garder le conteneur en cours d'exécution
tail -f /dev/null