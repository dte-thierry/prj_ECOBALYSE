#!/bin/bash

# Récupérer l'adresse IP publique de la VM
Public_IP=$(curl -s http://checkip.amazonaws.com)
Username=$(whoami)
SSH_Address="$Public_IP"

# Récupérer les constantes dans le conteneur
ECOBALYSE_VER=$(python3 /app/get_constants1.py ECOBALYSE_VER)
MONGODB_LOG_NAMEFILE=$(python3 /app/get_constants1.py MONGODB_LOG_NAMEFILE)
PROG_FULL_MODE=$(python3 /app/get_constants1.py PROG_FULL_MODE)
JSON_BASIC_FILE=$(python3 /app/get_constants1.py JSON_BASIC_FILE)
JSON_FULL_FILE=$(python3 /app/get_constants1.py JSON_FULL_FILE)

# Vérifier que les variables d'environnement sont définies
if [ -z "$JSON_BASIC_FILE" ] || [ -z "$JSON_FULL_FILE" ] || [ -z "$PROG_FULL_MODE" ]; then
  echo "Les variables d'environnement JSON_BASIC_FILE, JSON_FULL_FILE et PROG_FULL_MODE doivent être définies."
  exit 1
fi

# Afficher le message d'accueil
echo -e "------------------------------------------------------------"
echo -e "ETAPE 02 : Stockage des Données Ecobalyse $ECOBALYSE_VER via MongoDB"
echo -e "------------------------------------------------------------"
echo -e "VM utilisée, à l'adresse IP / SSH publique : $SSH_Address\n"

# Créer le répertoire de logs s'il n'existe pas
mkdir -p /app/logs

# Démarrer MongoDB en arrière-plan
mongod --bind_ip_all --fork --logpath /var/log/mongodb/mongod.log

# Attendre que MongoDB soit prêt
sleep 10

# Créer l'utilisateur admin si n'existe pas
mongo <<EOF
use admin
if (db.getUser("admin") === null) {
  db.createUser({
    user: "admin",
    pwd: "admin",
    roles: [{ role: "userAdminAnyDatabase", db: "admin" }]
  });
}
EOF

# Exécuter le script d'initialisation MongoDB
mongo /docker-entrypoint-initdb.d/init_mongo.js

# Exécuter le script de test
# /opt/venv/bin/python /app/test_mongo.py &> /app/logs/docker_testmongo_$(date +"%Y-%m-%d_%H-%M-%S").log
/opt/venv/bin/python /app/test_mongo.py &> /app/logs/${MONGODB_LOG_NAMEFILE}_$(date +"%Y-%m-%d_%H-%M-%S").log

# Message
echo -e "\nBase De Données MongoDB et fichier 'log' créés avec succès, par le conteneur.\n"

# Garder le conteneur en cours d'exécution
tail -f /dev/null