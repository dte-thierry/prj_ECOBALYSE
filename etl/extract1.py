# Charger les librairies utiles
from utils01 import get_ecobalyse_datas
from utils02 import get_description_datas
from utils03 import get_details_datas

import pandas as pd
import os

# Récupérer les variables d'environnement
PROG_FULL_MODE = os.getenv('PROG_FULL_MODE') == 'True'
JSON_BASIC_FILE = os.getenv('JSON_BASIC_FILE')
JSON_FULL_FILE = os.getenv('JSON_FULL_FILE')

# Récupérer les données de l'Explorateur Ecobalyse via : get_ecobalyse_datas()
url = 'https://ecobalyse.beta.gouv.fr/#/explore/textile'
columns = ['Nom', 'Categorie', 'ecs', 'pef', '.']
# Définir le chemin de sortie JSON en fonction du mode
if PROG_FULL_MODE:
    json_output_path = os.path.join('data', JSON_FULL_FILE)
else:
    json_output_path = os.path.join('data', JSON_BASIC_FILE)
# Récupérer les données
df = get_ecobalyse_datas(url, columns, json_output_path)


# Ajouter les descriptions des différents textiles via : get_description_datas()
params_dir = 'data'
api_token = "ed698f8f-e961-44a6-b9fa-dfaf3cf462ef"
# Définir le chemin de sortie JSON en fonction du mode
if PROG_FULL_MODE:
    json_output_path = os.path.join('data', JSON_FULL_FILE)
else:
    json_output_path = os.path.join('data', JSON_BASIC_FILE)
# Récupérer les descriptions
df_updated1 = get_description_datas(df, params_dir, api_token, json_output_path)


# Calculer les impacts détaillés des différents textiles via : get_details_datas()
params_dir = 'data'
api_token = "ed698f8f-e961-44a6-b9fa-dfaf3cf462ef"
# Définir le chemin de sortie JSON en fonction du mode
if PROG_FULL_MODE:
    json_output_path = os.path.join('data', JSON_FULL_FILE)
else:
    json_output_path = os.path.join('data', JSON_BASIC_FILE)
# Récupérer les détails
df_updated2 = get_details_datas(df_updated1, params_dir, api_token, json_output_path)
