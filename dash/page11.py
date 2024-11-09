# page11.py - Listing des données
from dash import html, dcc, callback, Input, Output, State, no_update
import dash
import dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import redis
import json

# Initialiser la connexion Redis
r = redis.Redis(host='ecblredis', port=6379, decode_responses=True, health_check_interval=30)

# Créer la mise en page de la page 11
def create_page11_layout():
    return html.Div([
        html.H1("Visualisation Des Données : Listing & Description", className='text-center my-4'),
        html.Div([
            html.Button('Charger les données', id='load-data-button'),
            dcc.Dropdown(id='category-dropdown', placeholder='Sélectionnez une catégorie', style={'width': '300px'}),
        ], style={'display': 'flex', 'gap': '10px'}),
        dash_table.DataTable(id='data-table', columns=[
            {'name': 'Libelle', 'id': 'Libelle'},
            {'name': 'Categorie', 'id': 'Categorie'},
            {'name': 'ecs', 'id': 'ecs'},
            # Ajouter d'autres colonnes si nécessaire
            {'name': 'Description', 'id': 'description'},
        ], data=[], style_table={'overflowX': 'auto'}),
    ], className='container', style={'background': 'beige', 'padding': '20px'})

@callback(
    Output('data-table', 'data'),
    Output('category-dropdown', 'options'),
    [Input('load-data-button', 'n_clicks'),
     Input('category-dropdown', 'value')]
)
def load_and_display_data(n_clicks, selected_category):
    if n_clicks is None:
        return [], []
    
    keys = r.keys('textile:*')
    data = []
    categories = set()
    for key in keys:
        textile_info = r.hgetall(key)
        data.append(textile_info)
        categories.add(textile_info.get('Categorie', 'N/A'))
    
    # Convertir les données en DataFrame pour faciliter le tri
    df = pd.DataFrame(data)
    df['ecs'] = pd.to_numeric(df['ecs'], errors='coerce')  # Convertir 'ecs' en numérique
    df = df.sort_values(by=['Categorie', 'ecs'], ascending=[True, True])  # Trier par 'Categorie' puis par 'ecs'
    
    # Filtrer les données par catégorie sélectionnée
    if selected_category:
        df = df[df['Categorie'] == selected_category]
    
    # Créer les options pour le Dropdown
    category_options = [{'label': category, 'value': category} for category in sorted(categories)]
    
    return df.to_dict('records'), category_options