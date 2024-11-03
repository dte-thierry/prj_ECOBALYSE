#!/bin/bash

# [-v] : affiche la version du client Docker installé
function show_version {
    echo -e "\nVersion du client Docker installé..."
    docker --version
}

# [-a] : affiche les conteneurs Docker en cours d'exécution
function show_containers {
    echo -e "\nListe les conteneurs Docker en cours d'exécution..."
    docker ps
}

# [-i] affiche la liste des images Docker présentes
function show_images {
    echo -e "\nListe des images Docker présentes..."
    docker images

    # Calcul de la taille totale des images Docker présentes
    total_size=0
    while read -r size unit; do
        if [ "$unit" == "GB" ]; then
            total_size=$(echo "$total_size + $size" | bc)
        elif [ "$unit" == "MB" ]; then
            size_in_gb=$(echo "scale=2; $size / 1024" | bc)
            total_size=$(echo "$total_size + $size_in_gb" | bc)
        fi
    done < <(docker images --format "{{.Size}}" | sed 's/ //g' | sed 's/GB/ GB/g' | sed 's/MB/ MB/g' | awk '{print $1, $2}')

    # echo -e "\nLa taille totale des images Docker est de ${total_size} GB.\n"
}

# [-all] : affiche toutes les informations
function show_all {
    show_version
    show_containers
    show_images
    show_logs
}

# [-df] : affiche l'espace disque disponible
function show_df {
    echo "Espace disque disponible : "
    df -h | egrep '(Filesystem|/dev/root)' | while read line; do
        echo -e "\t$line"
    done
}

# [-logs] : affiche les logs des conteneurs 'etl'
function show_logs {
    echo -e "\nAffichage des logs du conteneur : ecblwebscraping..."
    docker-compose logs ecblwebscraping
    echo -e "\nAffichage des logs du conteneur : ecblmongodb..."
    docker-compose logs ecblmongodb
    echo -e "\nAffichage des logs du conteneur : ecblredis..."
    docker-compose logs ecblredis
    # echo -e "\nAffichage des logs du conteneur : ecblflask..."
    # docker-compose logs ecblflask
}

# Récupérer l'adresse IP publique de la VM
Public_IP=$(curl -s http://checkip.amazonaws.com)
Username=$(whoami)
SSH_Address="$Public_IP"

# Récupérer les constantes ETL
ECOBALYSE_VER=$(python3 etl/get_constants.py ECOBALYSE_VER)
PROG_FULL_MODE=$(python3 etl/get_constants.py PROG_FULL_MODE)
PROG_NB_ITERATIONS=$(python3 etl/get_constants.py PROG_NB_ITERATIONS)
JSON_BASIC_FILE=$(python3 etl/get_constants.py JSON_BASIC_FILE)
JSON_FULL_FILE=$(python3 etl/get_constants.py JSON_FULL_FILE)

# Exporter les constantes pour qu'elles soient accessibles
export ECOBALYSE_VER
export PROG_FULL_MODE
export PROG_NB_ITERATIONS
export JSON_BASIC_FILE
export JSON_FULL_FILE

# Afficher le message d'accueil
echo -e "-----------------------------------------------------------"
echo -e "./info.sh : Informations diverses, et sur les conteneurs..."
echo -e "-----------------------------------------------------------"
echo -e "VM en cours, à l'adresse IP / SSH publique : $SSH_Address"

# Vérifier la valeur de PROG_FULL_MODE et préciser le fichier JSON à créer
if [ "$PROG_FULL_MODE" = "False" ]; then
    echo -e "\nMode d'Extraction Des Données Ecocalyse $ECOBALYSE_VER : Basic. \nFichier JSON utilisé : $JSON_BASIC_FILE"
elif [ "$PROG_FULL_MODE" = "True" ]; then
    echo -e "\nMode d'Extraction Des Données Ecocalyse $ECOBALYSE_VER : Complet. \nAjout et transformation de $PROG_NB_ITERATIONS donnée(s) aléatoire(s), par catégorie(s) de textile(s). \nFichier JSON utilisé : $JSON_FULL_FILE"
else
    echo -e "\nLa valeur de PROG_FULL_MODE n'est pas valide. Veuillez vérifier votre paramétrage ETL, avec la commande : ./mode.sh"
fi

# Analyser les options de ligne de commande
if [ "$1" == "-all" ]; then
    show_all
    exit 0
fi

if [ "$1" == "-df" ]; then
    show_df
    exit 0
fi

if [ "$1" == "-logs" ]; then
    show_logs
    exit 0
fi

while getopts "vai" opt; do
    case $opt in
        v)
            show_version
            exit 0
            ;;
        a)
            show_containers
            exit 0
            ;;
        i)
            show_images
            exit 0
            ;;
        *)
            echo "Usage: $0 [-v] [-a] [-i] [-all] [-df] [-logs]"
            exit 1
            ;;
    esac
done

# Si aucune option valide n'est fournie
echo "Usage: $0 [-v] [-a] [-i] [-all] [-df] [-logs]"
exit 1