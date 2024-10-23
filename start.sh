#!/bin/bash
sleep 3

# Vérifier si le script est exécuté dans un conteneur Docker
if grep -q docker /proc/1/cgroup; then
    # Exécution dans un conteneur Docker
    mkdir -p /app/logs
    echo "Pré-requis nécessaires au lancement par conteneur : "
    echo -e "\tvenv"
    echo -e "\tXvfb"
    source /app/venv/bin/activate    
    # Démarrer Xvfb et rediriger les erreurs vers /dev/null
    Xvfb :99 -screen 0 1920x1080x24 2>/dev/null &
    # Définir la variable d'environnement DISPLAY
    export DISPLAY=:99
    # Lancer Sélénium
    python3 /app/extract.py &> /app/logs/docker_webscraping_$(date +"%Y-%m-%d_%H-%M-%S").log
    echo "DataFrame, fichiers 'log' et 'json' créés avec succès par le conteneur."
else
    # Exécution en manuel
    mkdir -p logs
    echo "Pré-requis nécessaires au lancement manuel du script 'start.sh' : "
    echo -e "\t$(google-chrome --version)" # Afficher la version de Google Chrome
    echo -e "\t$(chromium --version)" # Afficher la version de Chromium
    echo -e "\t$(chromedriver --version)" # Afficher la version de ChromeDriver
    # Lancer Sélénium
    python3 etl/extract.py &> logs/manual_webscraping_$(date +"%Y-%m-%d_%H-%M-%S").log
    echo "DataFrame, fichiers 'log' et 'json' créés avec succès manuellement."
fi