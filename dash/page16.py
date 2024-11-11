# page16.py - Boxplot : Pays / ecs
from dash import html, dcc, callback, Input, Output, State, no_update
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import redis
import plotly.express as px

from components import create_message, create_boxplot

# Initialiser la connexion Redis
r = redis.Redis(host='ecblredis', port=6379, decode_responses=True, health_check_interval=30)
print("page-15 : Redis fonctionne et le fichier JSON est bien récupéré : ", r.ping())

# Lire les données depuis Redis et les convertir en DataFrame
keys = r.keys('textile:*')
data = []
for key in keys:
    textile_info = r.hgetall(key)
    data.append(textile_info)

# Convertir les données en DataFrame pour faciliter l'analyse
df = pd.DataFrame(data)

# Afficher les premières lignes du DataFrame pour vérifier les données
print(df.head())

# Afficher les colonnes du DataFrame pour vérifier la présence de 'ecs'
print("Colonnes du DataFrame :", df.columns)

# Convertir 'ecs' en numérique si la colonne existe
if 'ecs' in df.columns:
    df['ecs'] = pd.to_numeric(df['ecs'], errors='coerce')
else:
    print("La colonne 'ecs' n'existe pas dans le DataFrame.")

# Créer la mise en page de la page 16
def create_page16_layout():
    return html.Div([
        dcc.Store(id='page-id', data='page16'),
        html.H1("Boxplot : Pays / ecs", className='text-center my-4'),
        dcc.Graph(id='boxplot-graph'),

        create_message(["---"], style={'fontSize': 20}),
        create_message([
            "Ce Box Plot permet de voir les tendances centrales, la dispersion et les valeurs aberrantes, afin d'analyser l'impact environnemental des différents types de pays.",
            "La ligne horizontale à l'intérieur de chaque boîte représente la **médiane** des valeurs 'ecs' pour chaque catégorie.",
            "Les extrémités de la boîte représentent le **premier quartile (Q1)** et le **troisième quartile (Q3)**.",
            "La distance entre **Q1** et **Q3**, l'**étendue interquartile (IRQ)** donne une idée de la variabilité des valeurs 'ecs' pour chaque type de pays.",
            "Les points situés en dehors des *moustaches* sont des valeurs aberrantes (**outliers**)."                       
        ], style={'fontSize': 20}),
        create_message(["---"], style={'fontSize': 20})

    ], className='container', style={'background': 'beige', 'padding': '20px'})

