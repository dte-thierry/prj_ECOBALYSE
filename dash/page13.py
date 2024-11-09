# page13.py - Distribution cumulée de l'ecoscore 'ecs' par Catégories- de Textiles
from dash import html, dcc, callback, Input, Output, State, no_update
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import redis
import plotly.express as px

# Initialiser la connexion Redis
r = redis.Redis(host='ecblredis', port=6379, decode_responses=True, health_check_interval=30)
print("page-13 : Redis fonctionne et le fichier JSON est bien récupéré : ", r.ping())

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

# Vérifier la présence de la colonne 'Categorie'
if 'Categorie' in df.columns:
    # Ordonner les textiles par ecs et catégories croissant
    df = df.sort_values(by=['ecs', 'Categorie'])
else:
    print("La colonne 'Categorie' n'existe pas dans le DataFrame.")

# Créer la mise en page de la page 13
def create_page13_layout():
    return html.Div([
        html.H1("Distribution cumulée de l'ecoscore 'ecs' par Catégories de Textiles", className='text-center my-4'),
        dcc.Graph(id='distribution-graph')
    ], className='container', style={'background': 'beige', 'padding': '20px'})

# Callback pour mettre à jour le graphique de distribution
@callback(
    Output('distribution-graph', 'figure'),
    Input('distribution-graph', 'id')
)
def update_distribution_graph(_):
    # Créer le graphique de distribution     
    fig = px.bar(df, x='Categorie', y='ecs', color='Categorie',
                 title="Distribution cumulée de l'ecoscore 'ecs' par Catégories de Textiles",
                 labels={'ecs': "Valeur de l'écoscore 'ecs' (Pts)", 'Categorie': "Catégories"},
                 template='plotly_white')  

    # Améliorer la lisibilité du graphique
    fig.update_layout(
        xaxis_title="Catégories",
        yaxis_title="Valeur cumulée de l'écoscore 'ecs' (Pts)",
        legend_title="Catégories"        
    )  

    return fig