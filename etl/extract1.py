# Charger les librairies utiles
from utils01 import get_explorer_url, diviser_nom, extraire_masse, extraire_matiere
from utils01 import get_ecobalyse_datas
import pandas as pd
import time
import re

# Récupérer les données de l'Explorateur Ecobalyse via get_ecobalyse_datas()
url = 'https://ecobalyse.beta.gouv.fr/#/explore/textile'
columns = ['Nom', 'Categorie', 'ecs', 'pef', '.']
json_output_path = 'data/PRJ-ECOBALYSE-01-WEB_SCRAPING1_temp1.json'
df = get_ecobalyse_datas(url, columns, json_output_path)