#!/bin/bash

# Récupérer l'adresse IP publique de la VM
Public_IP=$(curl -s http://checkip.amazonaws.com)
Username=$(whoami)
SSH_Address="$Public_IP"

# Récupérer les constantes dans le conteneur
ECOBALYSE_VER=$(python3 /app/get_constants2.py ECOBALYSE_VER)
REDIS_LOG_NAMEFILE=$(python3 /app/get_constants2.py REDIS_LOG_NAMEFILE)
PROG_FULL_MODE=$(python3 /app/get_constants2.py PROG_FULL_MODE)
JSON_BASIC_FILE=$(python3 /app/get_constants2.py JSON_BASIC_FILE)
JSON_FULL_FILE=$(python3 /app/get_constants2.py JSON_FULL_FILE)

# Vérifier que les variables d'environnement sont définies
if [ -z "$JSON_BASIC_FILE" ] || [ -z "$JSON_FULL_FILE" ] || [ -z "$PROG_FULL_MODE" ]; then
  echo "Les variables d'environnement JSON_BASIC_FILE, JSON_FULL_FILE et PROG_FULL_MODE doivent être définies."
  exit 1
fi

# Définir le chemin du fichier JSON en fonction du mode
if [ "$PROG_FULL_MODE" = "True" ]; then
  json_file_path="/app/data/$JSON_FULL_FILE"
else
  json_file_path="/app/data/$JSON_BASIC_FILE"
fi

# Afficher le message d'accueil
echo -e "----------------------------------------------------------"
echo -e "ETAPE 02 : Stockage des Données Ecobalyse $ECOBALYSE_VER via Redis"
echo -e "----------------------------------------------------------"
echo -e "VM utilisée, à l'adresse IP / SSH publique : $SSH_Address\n"

# Créer le répertoire logs s'il n'existe pas
mkdir -p /app/logs

# Démarrer Redis en arrière-plan
redis-server /usr/local/etc/redis/redis.conf &

# Attendre que Redis soit prêt
sleep 5

# Attendre que le fichier JSON soit créé
echo -e "\nTest Redis de récupération JSON : "
echo -e "Attendre que le fichier JSON soit créé...\n"
while [ ! -f "$json_file_path" ]; do
  sleep 8
done

# Exécuter le script de test
# /opt/venv/bin/python /app/test_redis.py &> /app/logs/docker_testredis_$(date +"%Y-%m-%d_%H-%M-%S").log
/opt/venv/bin/python /app/test_redis.py &> /app/logs/${REDIS_LOG_NAMEFILE}_$(date +"%Y-%m-%d_%H-%M-%S").log

# message
echo -e "\nBase De Données Redis et fichier 'log' créés avec succès, par le conteneur.\n"

# Garder le conteneur en cours d'exécution
tail -f /dev/null