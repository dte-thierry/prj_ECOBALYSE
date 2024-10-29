#!/bin/bash

export FLASK_APP=test_flask.py
export FLASK_ENV=development

# Créer le répertoire logs s'il n'existe pas
mkdir -p logs

flask run --host=0.0.0.0