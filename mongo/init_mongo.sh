#!/bin/bash

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
/opt/venv/bin/python /app/test_mongo.py &> /app/logs/docker_testmongo_$(date +"%Y-%m-%d_%H-%M-%S").log

# Garder le conteneur en cours d'exécution
tail -f /dev/null