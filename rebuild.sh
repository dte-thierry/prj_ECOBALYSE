#!/bin/bash

# Reconstruire et redémarrer les services par 'docker-compose'
echo "Arrête, reconstruit, et redémarre les services ..."
docker-compose down
docker-compose up -d --build