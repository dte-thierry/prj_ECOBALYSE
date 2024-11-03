#!/bin/bash

# Fichier de constantes
CONSTANTS_FILE="etl/constants.py"

# Fonction pour afficher le mode (Basic | Complet) utilisé
function show_mode {
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

    if [ "$PROG_FULL_MODE" = "False" ]; then
        echo -e "\nMode d'Extraction Des Données Ecobalyse $ECOBALYSE_VER : Basic. \nFichier JSON utilisé : $JSON_BASIC_FILE"
    elif [ "$PROG_FULL_MODE" = "True" ]; then
        echo -e "\nMode d'Extraction Des Données Ecobalyse $ECOBALYSE_VER : Complet. \nAjout et transformation de $PROG_NB_ITERATIONS donnée(s) aléatoire(s), par catégorie(s) de textile(s). \nFichier JSON utilisé : $JSON_FULL_FILE"
    else
        echo -e "\nLa valeur de PROG_FULL_MODE n'est pas valide. Veuillez vérifier votre paramétrage ETL, avec la commande : ./mode.sh"
    fi
}

# Fonction pour modifier PROG_FULL_MODE
modify_prog_full_mode() {
    local mode=$1
    sed -i "s/^PROG_FULL_MODE = .*/PROG_FULL_MODE = $mode/" $CONSTANTS_FILE
}

# Fonction pour modifier PROG_NB_ITERATIONS
modify_prog_nb_iterations() {
    local iterations=$1
    sed -i "s/^PROG_NB_ITERATIONS = .*/PROG_NB_ITERATIONS = $iterations/" $CONSTANTS_FILE
}

# Récupérer l'adresse IP publique de la VM
Public_IP=$(curl -s http://checkip.amazonaws.com)
Username=$(whoami)
SSH_Address="$Public_IP"

# Afficher le message d'accueil
echo -e "-----------------------------------------------------------------"
echo -e "./mode.sh : Définit le mode d'extraction des données Ecobalyse..."
echo -e "-----------------------------------------------------------------"
echo -e "VM en cours, à l'adresse IP / SSH publique : $SSH_Address"

# Vérification des options
if [ "$1" == "-f" ]; then
    modify_prog_full_mode "True"

    echo -e "Pour le mode d'extraction \"complet\", avec création de 'n' données aléatoires... \n\tveuillez saisir un nombre 'n' (entre 1 et 30000) : "
    read input

    if [[ $input =~ ^[0-9]+$ ]] && [ "$input" -ge 1 ] && [ "$input" -le 30000 ]; then
        modify_prog_nb_iterations "$input"
        show_mode
    else
        echo -e "\nErreur : Veuillez saisir un nombre 'n' valide, entre 1 et 30000."
        modify_prog_nb_iterations "1"
    fi
else
    modify_prog_full_mode "False"
    show_mode
fi