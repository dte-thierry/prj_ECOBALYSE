# page13.py - Courbe d'estimation de densité de la variable 'ecs'
from dash import html, dcc, callback, Input, Output, State, no_update
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import redis
import plotly.express as px
import plotly.graph_objects as go

from components import create_message

# Initialiser la connexion Redis
r = redis.Redis(host='ecblredis', port=6379, decode_responses=True, health_check_interval=30)
print("page-13 : Redis fonctionne et le fichier JSON est bien récupéré : ", r.ping())

# Créer la mise en page de la page 13
def create_page13_layout():
    return html.Div([
        html.H1("Courbe d'estimation de densité de la variable 'ecs'", className='text-center my-4'),
        dcc.Graph(id='density-graph'),
        create_message(["---"], style={'fontSize': 20}),
        create_message([
            "Ce graphique montre : *la distribution de la variable 'ecs'*.",
            "On observe une concentration élevée de valeurs, autour d'un *'ecoscore'* de 2000 Pts.",
            "Ce qui signifie qu'une grande majorité de textiles, dans ce jeu de données, a un impact environnemental <= 2000 Pts."
        ], style={'fontSize': 20}),
        create_message(["---"], style={'fontSize': 20})
    ], className='container', style={'background': 'beige', 'padding': '20px'})


def display_density_graph(pathname):
    if pathname != '/page-13':
        return no_update
    
    keys = r.keys('textile:*')
    data = []
    for key in keys:
        textile_info = r.hgetall(key)
        data.append(textile_info)
    
    # Convertir les données en DataFrame pour faciliter l'analyse
    df = pd.DataFrame(data)
    df['ecs'] = pd.to_numeric(df['ecs'], errors='coerce')  # Convertir 'ecs' en numérique
    
    # Créer le graphique de la courbe d'estimation de densité de la variable 'ecs'
    fig = go.Figure()

    # Ajouter l'histogramme
    fig.add_trace(go.Histogram(x=df['ecs'], nbinsx=10, name='Histogramme'))

    # Ajouter la courbe d'estimation de densité
    kde_fig = px.histogram(df, x='ecs', nbins=10, histnorm='density', marginal='rug')
    for trace in kde_fig.data:
        fig.add_trace(trace)

    # Mettre à jour les titres et les étiquettes
    fig.update_layout(title="Courbe d'estimation de densité de la variable 'ecs'",
                      xaxis_title="Ecoscore 'ecs' (Pts)",
                      yaxis_title="Densité",
                      barmode='overlay')
    
    return fig
