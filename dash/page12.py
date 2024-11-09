# page12.py - Nombre de textiles par catégories
from dash import html, dcc, callback, Input, Output, State, no_update
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import redis
import json
import plotly.express as px

# Initialiser la connexion Redis
r = redis.Redis(host='ecblredis', port=6379, decode_responses=True, health_check_interval=30)

# Créer la mise en page de la page 12
def create_page12_layout():
    return html.Div([
        html.H1("Nombre de Textiles par Catégories", className='text-center my-4'),
        dcc.Graph(id='category-count-graph')
    ], className='container', style={'background': 'beige', 'padding': '20px'})

@callback(
    Output('category-count-graph', 'figure'),
    [Input('category-count-graph', 'id')]
)
def display_graph(_):
    keys = r.keys('textile:*')
    data = []
    for key in keys:
        textile_info = r.hgetall(key)
        data.append(textile_info)
    
    # Convertir les données en DataFrame pour faciliter l'analyse
    df = pd.DataFrame(data)
    df['ecs'] = pd.to_numeric(df['ecs'], errors='coerce')  # Convertir 'ecs' en numérique
    
    # Créer le graphique du nombre de textiles par catégories
    count_df = df['Categorie'].value_counts().reset_index()
    count_df.columns = ['Categorie', 'Nombre de textiles']
    fig = px.bar(count_df, x='Categorie', y='Nombre de textiles',
                 title='Nombre de Textiles par Catégories',
                 labels={'Categorie': 'Catégorie', 'Nombre de textiles': 'Nombre de Textiles'},
                 text_auto=True)
    
    return fig