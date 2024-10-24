# Charger les librairies utiles
from utils01 import get_ecobalyse_datas
from utils02 import get_description_datas

import pandas as pd

# Récupérer les données de l'Explorateur Ecobalyse : via get_ecobalyse_datas()
url = 'https://ecobalyse.beta.gouv.fr/#/explore/textile'
columns = ['Nom', 'Categorie', 'ecs', 'pef', '.']
json_output_path = 'data/PRJ-ECOBALYSE-01-WEB_SCRAPING1_temp1.json'
df = get_ecobalyse_datas(url, columns, json_output_path)

# Ajouter les descriptions des différents textiles via : get_description_datas()
params_dir = 'data'
api_token = "ed698f8f-e961-44a6-b9fa-dfaf3cf462ef"
json_output_path = 'data/PRJ-ECOBALYSE-01-WEB_SCRAPING1_temp1.json'
df_updated1 = get_description_datas(df, params_dir, api_token, json_output_path)