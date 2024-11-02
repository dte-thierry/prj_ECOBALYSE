#!/bin/bash
sleep 3

# Récupérer l'adresse IP publique de la VM
Public_IP=$(curl -s http://checkip.amazonaws.com)
Username=$(whoami)
# SSH_Address="$Username@$Public_IP"
SSH_Address="$Public_IP"

# Fonction pour afficher le message d'avertissement
function show_warning {
    echo -e "\nAvertissement:"
    echo -e "--------------"
    echo -e "L'API d'Ecobalyse est actuellement non finalisée, toujours en cours de développement."
    echo -e "Ce projet se base sur l'API d'Ecobalyse : $ECOBALYSE_VER pour récupérer les données."
    echo -e "Soyez attentif et vigilant à la récupération des données Ecobalyse obtenues, via l'API."
    echo -e "Consultez dans le répertoire /logs, le fichier .log : $WEBSCRAPING_LOG_FILE."
    echo -e "Vérifiez qu'aucune description de textile (colonne 'description') ne soit de type : NaN\n"
}

# ---------------------------------------------------------------------------------------
# Exécution dans un conteneur Docker
# ---------------------------------------------------------------------------------------

# Vérifier si le script est exécuté dans un conteneur Docker
if grep -q docker /proc/1/cgroup; then

    # Exécution dans un conteneur Docker
    mkdir -p /app/logs
    mkdir -p /app/data    
    source /app/venv/bin/activate   

    # Démarrer Xvfb et rediriger les erreurs vers /dev/null
    Xvfb :99 -screen 0 1920x1080x24 2>/dev/null &

    # Définir la variable d'environnement DISPLAY
    export DISPLAY=:99

    # Récupérer les constantes dans le conteneur
    ECOBALYSE_VER=$(python3 /app/get_constants.py ECOBALYSE_VER)
    WEBSCRAPING_LOG_FILE=$(python3 /app/get_constants.py WEBSCRAPING_LOG_FILE)
    PROG_FULL_MODE=$(python3 /app/get_constants.py PROG_FULL_MODE)
    JSON_BASIC_FILE=$(python3 /app/get_constants.py JSON_BASIC_FILE)
    JSON_FULL_FILE=$(python3 /app/get_constants.py JSON_FULL_FILE)
    
    # Vérifier que les variables d'environnement sont définies
    if [ -z "$JSON_BASIC_FILE" ] || [ -z "$JSON_FULL_FILE" ] || [ -z "$PROG_FULL_MODE" ]; then
        echo "Les variables d'environnement JSON_BASIC_FILE, JSON_FULL_FILE et PROG_FULL_MODE doivent être définies."
        exit 1
    fi
    
    # Afficher les informations de base
    echo -e "--------------------------------------------------------------"
    echo -e "ETAPE 01 : Récupération des Données via l'API Ecobalyse $ECOBALYSE_VER"
    echo -e "--------------------------------------------------------------"
    echo -e "VM utilisée, à l'adresse IP / SSH publique : $SSH_Address"
    
    # Vérifier la valeur de PROG_FULL_MODE et préciser le fichier JSON à créer
    if [ "$PROG_FULL_MODE" = "False" ]; then
        echo -e "\nMode d'Extraction Des Données : Basic. \nFichier JSON à créer : $JSON_BASIC_FILE"
    elif [ "$PROG_FULL_MODE" = "True" ]; then
        echo -e "\nMode d'Extraction Des Données : Complet, avec ajout et transformation de données aléatoires. \nFichier JSON à créer : $JSON_FULL_FILE"
    else
        echo -e "\nLa valeur de PROG_FULL_MODE n'est pas valide. Veuillez vérifier votre paramétrage ETL."
    fi

    # Lancer Sélénium
    python3 /app/extract1.py &> /app/logs/docker_webscraping_$(date +"%Y-%m-%d_%H-%M-%S").log
    
    # résultat : vérifier la valeur de PROG_FULL_MODE et préciser le fichier JSON créé
    if [ "$PROG_FULL_MODE" = "False" ]; then
        echo -e "\nDataFrame, fichiers 'log' et 'json' $JSON_BASIC_FILE créés avec succès, en mode basic."
    elif [ "$PROG_FULL_MODE" = "True" ]; then
        echo -e "\nDataFrame, fichiers 'log' et 'json' $JSON_FULL_FILE créés avec succès, en mode complet."
    else
        echo -e "\nPar défaut, le fichier $JSON_BASIC_FILE a été créé, en mode basic."
    fi

    echo -e "\n"

# ---------------------------------------------------------------------------------------
# Exécution standard
# ---------------------------------------------------------------------------------------

else
    # Exécution standard
    mkdir -p logs
    mkdir -p data
    sudo chmod -R 777 logs
    sudo chmod -R 777 data

    # Récupérer les constantes en manuel
    ECOBALYSE_VER=$(python3 etl/get_constants.py ECOBALYSE_VER)
    WEBSCRAPING_LOG_FILE=$(python3 etl/get_constants.py WEBSCRAPING_LOG_FILE)
    PROG_FULL_MODE=$(python3 etl/get_constants.py PROG_FULL_MODE)
    PROG_ADM_RULE=$(python3 etl/get_constants.py PROG_ADM_RULE)
    PROG_NB_ITERATIONS=$(python3 etl/get_constants.py PROG_NB_ITERATIONS)
    JSON_BASIC_FILE=$(python3 etl/get_constants.py JSON_BASIC_FILE)
    JSON_FULL_FILE=$(python3 etl/get_constants.py JSON_FULL_FILE)

    # Exporter les constantes pour qu'elles soient accessibles
    export PROG_FULL_MODE
    export PROG_ADM_RULE
    export PROG_NB_ITERATIONS
    export JSON_BASIC_FILE
    export JSON_FULL_FILE

    # Afficher les informations de base
    echo -e "--------------------------------------------------------------"
    echo -e "ETAPE 01 : Récupération des Données via l'API Ecobalyse $ECOBALYSE_VER"
    echo -e "--------------------------------------------------------------"
    echo -e "VM utilisée, à l'adresse IP / SSH publique : $SSH_Address"
    
    # Vérifier la valeur de PROG_FULL_MODE et préciser le fichier JSON à créer
    if [ "$PROG_FULL_MODE" = "False" ]; then
        echo -e "\nMode d'Extraction Des Données : Basic. \nFichier JSON à créer : $JSON_BASIC_FILE"
    elif [ "$PROG_FULL_MODE" = "True" ]; then
        echo -e "\nMode d'Extraction Des Données : Complet, avec ajout et transformation de données aléatoires. \nFichier JSON à créer : $JSON_FULL_FILE"
    else
        echo -e "\nLa valeur de PROG_FULL_MODE n'est pas valide. Veuillez vérifier votre paramétrage ETL."
    fi
    
    # Analyser les options de la ligne de commande
    while getopts "i" opt; do
        case $opt in
            i)
                show_warning
                # exit 0            
                ;;
            \?)
                echo "Usage: $0 [-i]"
                exit 1
                ;;
        esac
    done

    # Lancer Sélénium
    python3 etl/extract1.py &> logs/manual_webscraping_$(date +"%Y-%m-%d_%H-%M-%S").log

    # résultat : vérifier la valeur de PROG_FULL_MODE et préciser le fichier JSON créé
    if [ "$PROG_FULL_MODE" = "False" ]; then
        echo -e "\nDataFrame, fichiers 'log' et 'json' $JSON_BASIC_FILE créés avec succès, en mode basic."
    elif [ "$PROG_FULL_MODE" = "True" ]; then
        echo -e "\nDataFrame, fichiers 'log' et 'json' $JSON_FULL_FILE créés avec succès, en mode complet."
    else
        echo -e "\nPar défaut, le fichier $JSON_BASIC_FILE a été créé, en mode basic."
    fi

    echo -e "\n"
fi