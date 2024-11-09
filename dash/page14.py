# page14.py - Densité estimée & répartition cumulée de la variable 'ecs'
from dash import html, dcc, callback, Input, Output, State, no_update
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import redis

# import json

# import plotly.express as px
# import plotly.graph_objects as go

# Initialiser la connexion Redis
r = redis.Redis(host='ecblredis', port=6379, decode_responses=True, health_check_interval=30)
print("page-14 : Redis fonctionne et le fichier JSON est bien récupéré : ", r.ping())

# Créer la mise en page de la page 14
def create_page14_layout():
    return html.Div([
        html.H1("Densité estimée & répartition cumulée de la variable 'ecs'", className='text-center my-4'),
        # dcc.Graph(id='density-graph')
    ], className='container', style={'background': 'beige', 'padding': '20px'})

"""
@callback(
    Output('density-graph', 'figure'),
    [Input('density-graph', 'id')]
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
    
    # Créer le graphique de la courbe d'estimation de densité de la variable 'ecs'
    fig = go.Figure()
    
    # Ajouter l'histogramme
    fig.add_trace(go.Histogram(x=df['ecs'], nbinsx=10, name='Histogramme'))
    
    # Ajouter la courbe d'estimation de densité
    fig.add_trace(go.Histogram(x=df['ecs'], nbinsx=10, histnorm='probability density', name='Densité', marker_color='red'))
    
    # Ajouter le rug plot
    fig.add_trace(go.Scatter(x=df['ecs'], y=[0]*len(df), mode='markers', marker=dict(color='red'), name='Rug Plot'))
    
    # Mettre à jour les titres et les étiquettes
    fig.update_layout(title="Courbe d'estimation de densité de la variable 'ecs'",
                      xaxis_title="Ecoscore 'ecs' (Pts)",
                      yaxis_title="Densité",
                      barmode='overlay')
    
    return fig
"""