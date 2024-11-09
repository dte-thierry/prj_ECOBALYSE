# page14.py - Densité estimée & répartition cumulée de la variable 'ecs'
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
print("page-14 : Redis fonctionne et le fichier JSON est bien récupéré : ", r.ping())

# Créer la mise en page de la page 14
def create_page14_layout():
    return html.Div([
        html.H1("Densité estimée & répartition cumulée de la variable 'ecs'", className='text-center my-4'),
        dcc.Graph(id='density-graph-14'),

        create_message(["---"], style={'fontSize': 20}),
        create_message([
            "Le graphique ci-dessus montre : *la distribution, et la densité estimée de la variable 'ecs'*.",
            "On observe une forte densité, et une concentration élevée de valeurs, autour d'un *'ecoscore'* de 2000 Pts.",
            "Ce qui signifie qu'une grande majorité de textiles, dans ce jeu de données, a un impact environnemental <= 2000 Pts."
        ], style={'fontSize': 20}),
        create_message(["---"], style={'fontSize': 20}),

        dcc.Graph(id='ecdf-graph'), 

        create_message(["---"], style={'fontSize': 20}),
        create_message([
            "Le graphique ci-dessus montre : la *répartition cumulée empirique (ECDF)* de la variable 'ecs'.",
            "la **courbe ECDF** (Empirical Cumulative Distribution Function) de distribution cumulative, commence à zéro et augmente par paliers pour atteindre 1.0 à droite.", 
            "Cette courbe montre la proportion cumulative de l'ecoscore 'ecs'.",
            "Les paliers significatifs se trouvent autour de 2500, 5000, 7500, et juste avant 10000.",
            "Une grande proportion des observations a une valeur 'ecs' inférieure ou égale à 2500 Pts.",
            "La courbe atteignant 1.0, indique que toutes les observations sont incluses à la fin."
        ], style={'fontSize': 20}),
        create_message(["---"], style={'fontSize': 20})

    ], className='container', style={'background': 'beige', 'padding': '20px'})

def display_graph(pathname):
    if pathname != '/page-14':
        return no_update, no_update
    
    keys = r.keys('textile:*')
    data = []
    for key in keys:
        textile_info = r.hgetall(key)
        data.append(textile_info)
    
    # Convertir les données en DataFrame pour faciliter l'analyse
    df = pd.DataFrame(data)
    df['ecs'] = pd.to_numeric(df['ecs'], errors='coerce')  # Convertir 'ecs' en numérique
    
    # Créer le graphique de l'estimation de densité par noyaux (KDE)
    kde_fig = px.histogram(df, x='ecs', nbins=10, histnorm='density', marginal='rug')
    kde_fig.update_layout(title="Estimation de la densité par noyaux (KDE)",
                          xaxis_title="Ecoscore 'ecs' (Pts)",
                          yaxis_title="Densité")
    
    # Créer le graphique de la répartition cumulée empirique (ECDF)
    ecdf_fig = px.ecdf(df, x='ecs')
    ecdf_fig.update_layout(title="Répartition cumulée de la variable 'ecs'",
                           xaxis_title="Ecoscore 'ecs' (Pts)",
                           yaxis_title="Proportion")
    
    return kde_fig, ecdf_fig