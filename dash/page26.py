# page26.py - jupe
from dash import html, dcc, callback, Input, Output, State, no_update
import dash
import pandas as pd
import joblib

import dash_bootstrap_components as dbc

# Charger le modèle
pipeline_loaded = joblib.load('./assets/linear_regression_model_basic.pkl')

# Lire le contenu des fichiers d'informations paramètres
with open('./assets/info_masse.txt', 'r') as file:
    info_masse_content = file.read()
with open('./assets/info_matiere.txt', 'r') as file:
    info_matiere_content = file.read()
with open('./assets/info_mode.txt', 'r') as file:
    info_mode_content = file.read()
with open('./assets/info_pays.txt', 'r') as file:
    info_pays_content = file.read()
with open('./assets/info_product.txt', 'r') as file:
    info_product_content = file.read()    
with open('./assets/info_countrySpinning.txt', 'r') as file:
    info_countrySpinning_content = file.read()
with open('./assets/info_countryFabric.txt', 'r') as file:
    info_countryFabric_content = file.read()
with open('./assets/info_countryDyeing.txt', 'r') as file:
    info_countryDyeing_content = file.read()
with open('./assets/info_countryMaking.txt', 'r') as file:
    info_countryMaking_content = file.read()

# Créer la mise en page de la page 26
def create_page26_layout():
    return html.Div([
        html.H1("Prédiction d'ecoscore 'ecs', pour la catégorie : Jupe / Robe", className='text-center my-4'),
        
        html.Div([
            html.Div([
                html.Label('Libelle', className='form-label'),
                dcc.Input(id='libelle', type='text', value='Jupe / Robe (exemple ML)', className='form-control', readOnly=True),
            ], className='mb-3'),
            
            html.Div([ 
                html.Label('Masse (en kg. Min 0.15 | Max 0.50)', className='form-label'),
                dcc.Input(id='masse', type='number', value=0.30, min=0.15, max=0.50, step=0.05, className='form-control'),
                dbc.Tooltip(
                    info_masse_content,
                    target="masse",
                    placement="right",
                    trigger="click hover",
                    className='custom-tooltip'  # Appliquer la classe CSS personnalisée  
                )
            ], className='mb-3'),
            
            html.Div([
                html.Label("Pays, pour les étapes de transformation (filature, tissage/tricotage, ennoblissement et confection)", className='form-label'),
                # dcc.Input(id='pays', type='text', value='Pays inconnu', className='form-control'),
                dcc.Dropdown(
                    id='pays',
                    options=[
                      # {'label': 'Afrique | RAF', 'value': 'Afrique'},
                      # {'label': 'Albanie | AL', 'value': 'Albanie'},
                      # {'label': 'Allemagne | DE', 'value': 'Allemagne'},
                      # {'label': 'Amérique du Nord | RNA', 'value': 'Amerique du Nord'},
                      # {'label': 'Amérique Latine | RLA', 'value': 'Amerique Latine'},
                        {'label': 'Asie | RAS', 'value': 'Asie'},
                      # {'label': 'Bangladesh | BD', 'value': 'Bangladesh'},
                      # {'label': 'Belgique | BE', 'value': 'Belgique'},
                      # {'label': 'Cambodge | KH', 'value': 'Cambodge'},
                        {'label': 'Chine | CN', 'value': 'Chine'},
                      # {'label': 'Egypte | EG', 'value': 'Egypte'},
                      # {'label': 'Espagne | ES', 'value': 'Espagne'},
                      # {'label': 'Ethiopie | ET', 'value': 'Ethiopie'},
                      # {'label': "Europe de l'Est | REE", 'value': "Europe de l'Est"},
                      # {'label': "Europe de l'Ouest | REO", 'value': "Europe de l'Ouest"},
                        {'label': 'France | FR', 'value': 'France'},
                      # {'label': 'Grèce | GR', 'value': 'Grece'},
                      # {'label': 'Hongrie | HU', 'value': 'Hongrie'},
                      # {'label': 'Inde | IN', 'value': 'Inde'},
                      # {'label': 'Italie | IT', 'value': 'Italie'},
                      # {'label': 'Maroc | MA', 'value': 'Maroc'},
                      # {'label': 'Moyen-Orient | RME', 'value': 'Moyen-Orient'},
                      # {'label': 'Myanmar | MM', 'value': 'Myanmar'},
                      # {'label': 'Océanie | ROC', 'value': 'Oceanie'},
                        {'label': 'Pakistan | PK', 'value': 'Pakistan'},
                      # {'label': 'Pologne | PL', 'value': 'Pologne'},
                      # {'label': 'Portugal | PT', 'value': 'Portugal'},
                      # {'label': 'Pays-Bas | NL', 'value': 'Pays-Bas'},
                        {'label': 'Pays inconnu | ---', 'value': 'Pays inconnu'}
                      # {'label': 'Roumanie | RO', 'value': 'Roumanie'},
                      # {'label': 'Royaume-Uni | GB', 'value': 'Royaume-Uni'},
                      # {'label': 'Sri Lanka | LK', 'value': 'Sri Lanka'},
                      # {'label': 'Suisse | CH', 'value': 'Suisse'},
                      # {'label': 'Taiwan | TW', 'value': 'Taiwan'},
                      # {'label': 'Tchéquie | CZ', 'value': 'Tchequie'},
                      # {'label': 'Tunisie | TN', 'value': 'Tunisie'},
                      # {'label': 'Turquie | TR', 'value': 'Turquie'},
                      # {'label': 'Vietnam | VN', 'value': 'Vietnam'}                      
                    ],
                    value='Pays inconnu',
                    className='form-control'
                ),
                dbc.Tooltip(
                    info_pays_content,
                    target="pays",
                    placement="right",
                    trigger="click hover",
                    className='custom-tooltip'  # Appliquer la classe CSS personnalisée  
                )
            ], className='mb-3'),

            html.Div([
                html.Label('Matiere', className='form-label'),
                # dcc.Input(id='matiere', type='text', value='coton', className='form-control'),
                dcc.Dropdown(
                    id='matiere',
                    options=[
                        {'label': 'coton', 'value': 'coton'},
                        {'label': 'coton bio', 'value': 'coton bio'},
                      # {'label': 'laine', 'value': 'laine'},
                        {'label': 'laine paysanne', 'value': 'laine paysane'},
                        {'label': 'lin', 'value': 'lin'},
                        {'label': 'polyester', 'value': 'polyester'},
                        {'label': 'synthétique', 'value': 'synthetique'}
                      # {'label': 'viscose', 'value': 'viscose'}
                    ],
                    value='coton',
                    className='form-control'
                ),
                dbc.Tooltip(
                    info_matiere_content,
                    target="matiere",
                    placement="right",
                    trigger="click hover",
                    className='custom-tooltip'  # Appliquer la classe CSS personnalisée  
                )
            ], className='mb-3'),
            
            html.Div([
                html.Label('Mode', className='form-label'),
                # dcc.Input(id='mode', type='text', value='Majorant par defaut', className='form-control'),
                dcc.Dropdown(
                    id='mode',
                    options=[
                        {'label': 'Majorant par défaut', 'value': 'Majorant par defaut'},
                        {'label': 'Mode éthique', 'value': 'Mode ethique'},
                        {'label': 'Mode fast fashion', 'value': 'Mode fast fashion'},
                        {'label': 'Mode traditionnelle', 'value': 'Mode traditionnelle'},
                        {'label': 'Mode ultra fast fashion', 'value': 'Mode ultra fast fashion'}
                    ],
                    value='Majorant par defaut',
                    className='form-control'
                ),
                dbc.Tooltip(
                    info_mode_content,
                    target="mode",
                    placement="right",
                    trigger="click hover",
                    className='custom-tooltip'  # Appliquer la classe CSS personnalisée  
                )
            ], className='mb-3'),
            
            html.Div([
                html.Label('product, (Identifiant du produit)', className='form-label'),
                dcc.Input(id='product', type='text', value='jupe', className='form-control', readOnly=True),
                dbc.Tooltip(
                    info_product_content,
                    target="product",
                    placement="right",
                    trigger="click hover",
                    className='custom-tooltip'  # Appliquer la classe CSS personnalisée  
                )
            ], className='mb-3'),
            
            html.Div([
                html.Label("Country Spinning, (Code pays pour l'étape de Filature)", className='form-label'),
                # dcc.Input(id='countrySpinning', type='text', value='---', className='form-control'),
                dcc.Dropdown(
                    id='countrySpinning',
                    options=[
                      # {'label': 'RAF', 'value': 'RAF'},
                      # {'label': 'AL', 'value': 'AL'},
                      # {'label': 'DE', 'value': 'DE'},
                      # {'label': 'RNA', 'value': 'RNA'},
                      # {'label': 'RLA', 'value': 'RLA'},
                        {'label': 'RAS', 'value': 'RAS'},
                      # {'label': 'BD', 'value': 'BD'},
                      # {'label': 'BE', 'value': 'BE'},
                      # {'label': 'KH', 'value': 'KH'},
                        {'label': 'CN', 'value': 'CN'},
                      # {'label': 'EG', 'value': 'EG'},
                      # {'label': 'ES', 'value': 'ES'},
                      # {'label': 'ET', 'value': 'ET'},
                      # {'label': "REE", 'value': "REE"},
                      # {'label': "REO", 'value': "REO"},
                        {'label': 'FR', 'value': 'FR'},
                      # {'label': 'GR', 'value': 'GR'},
                      # {'label': 'HU', 'value': 'HU'},
                      # {'label': 'IN', 'value': 'IN'},
                      # {'label': 'IT', 'value': 'IT'},
                      # {'label': 'MA', 'value': 'MA'},
                      # {'label': 'RME', 'value': 'RME'},
                      # {'label': 'MM', 'value': 'MM'},
                      # {'label': 'ROC', 'value': 'ROC'},
                        {'label': 'PK', 'value': 'PK'},
                      # {'label': 'PL', 'value': 'PL'},
                      # {'label': 'PT', 'value': 'PT'},
                      # {'label': 'NL', 'value': 'NL'},
                        {'label': '---', 'value': '---'},
                      # {'label': 'RO', 'value': 'RO'},
                      # {'label': 'GB', 'value': 'GB'},
                      # {'label': 'LK', 'value': 'LK'},
                      # {'label': 'CH', 'value': 'CH'},
                      # {'label': 'TW', 'value': 'TW'},
                      # {'label': 'CZ', 'value': 'CZ'},
                      # {'label': 'TN', 'value': 'TN'},
                        {'label': 'TR', 'value': 'TR'}
                      # {'label': 'VN', 'value': 'VN'}                      
                    ],
                    value='---',
                    className='form-control'
                ),
                dbc.Tooltip(
                    info_countrySpinning_content,
                    target="countrySpinning",
                    placement="right",
                    trigger="click hover",
                    className='custom-tooltip'  # Appliquer la classe CSS personnalisée  
                )
            ], className='mb-3'),
            
            html.Div([
                html.Label("Country Fabric, (Code pays pour l'étape de Tissage/Tricotage)", className='form-label'),
                # dcc.Input(id='countryFabric', type='text', value='---', className='form-control'),
                dcc.Dropdown(
                    id='countryFabric',
                    options=[
                      # {'label': 'RAF', 'value': 'RAF'},
                      # {'label': 'AL', 'value': 'AL'},
                      # {'label': 'DE', 'value': 'DE'},
                      # {'label': 'RNA', 'value': 'RNA'},
                      # {'label': 'RLA', 'value': 'RLA'},
                        {'label': 'RAS', 'value': 'RAS'},
                      # {'label': 'BD', 'value': 'BD'},
                      # {'label': 'BE', 'value': 'BE'},
                      # {'label': 'KH', 'value': 'KH'},
                        {'label': 'CN', 'value': 'CN'},
                      # {'label': 'EG', 'value': 'EG'},
                      # {'label': 'ES', 'value': 'ES'},
                      # {'label': 'ET', 'value': 'ET'},
                      # {'label': "REE", 'value': "REE"},
                      # {'label': "REO", 'value': "REO"},
                        {'label': 'FR', 'value': 'FR'},
                      # {'label': 'GR', 'value': 'GR'},
                      # {'label': 'HU', 'value': 'HU'},
                      # {'label': 'IN', 'value': 'IN'},
                      # {'label': 'IT', 'value': 'IT'},
                      # {'label': 'MA', 'value': 'MA'},
                      # {'label': 'RME', 'value': 'RME'},
                      # {'label': 'MM', 'value': 'MM'},
                      # {'label': 'ROC', 'value': 'ROC'},
                        {'label': 'PK', 'value': 'PK'},
                      # {'label': 'PL', 'value': 'PL'},
                      # {'label': 'PT', 'value': 'PT'},
                      # {'label': 'NL', 'value': 'NL'},
                        {'label': '---', 'value': '---'}
                      # {'label': 'RO', 'value': 'RO'},
                      # {'label': 'GB', 'value': 'GB'},
                      # {'label': 'LK', 'value': 'LK'},
                      # {'label': 'CH', 'value': 'CH'},
                      # {'label': 'TW', 'value': 'TW'},
                      # {'label': 'CZ', 'value': 'CZ'},
                      # {'label': 'TN', 'value': 'TN'},
                      # {'label': 'TR', 'value': 'TR'},
                      # {'label': 'VN', 'value': 'VN'}                      
                    ],
                    value='---',
                    className='form-control'
                ),
                dbc.Tooltip(
                    info_countryFabric_content,
                    target="countryFabric",
                    placement="right",
                    trigger="click hover",
                    className='custom-tooltip'  # Appliquer la classe CSS personnalisée  
                )
            ], className='mb-3'),
            
            html.Div([
                html.Label("Country Dyeing, (Code pays pour l'étape de Teinture)", className='form-label'),
                # dcc.Input(id='countryDyeing', type='text', value='---', className='form-control'),
                dcc.Dropdown(
                    id='countryDyeing',
                    options=[
                      # {'label': 'RAF', 'value': 'RAF'},
                      # {'label': 'AL', 'value': 'AL'},
                      # {'label': 'DE', 'value': 'DE'},
                      # {'label': 'RNA', 'value': 'RNA'},
                      # {'label': 'RLA', 'value': 'RLA'},
                        {'label': 'RAS', 'value': 'RAS'},
                      # {'label': 'BD', 'value': 'BD'},
                      # {'label': 'BE', 'value': 'BE'},
                      # {'label': 'KH', 'value': 'KH'},
                        {'label': 'CN', 'value': 'CN'},
                      # {'label': 'EG', 'value': 'EG'},
                      # {'label': 'ES', 'value': 'ES'},
                      # {'label': 'ET', 'value': 'ET'},
                      # {'label': "REE", 'value': "REE"},
                      # {'label': "REO", 'value': "REO"},
                        {'label': 'FR', 'value': 'FR'},
                      # {'label': 'GR', 'value': 'GR'},
                      # {'label': 'HU', 'value': 'HU'},
                      # {'label': 'IN', 'value': 'IN'},
                      # {'label': 'IT', 'value': 'IT'},
                      # {'label': 'MA', 'value': 'MA'},
                      # {'label': 'RME', 'value': 'RME'},
                      # {'label': 'MM', 'value': 'MM'},
                      # {'label': 'ROC', 'value': 'ROC'},
                        {'label': 'PK', 'value': 'PK'},
                      # {'label': 'PL', 'value': 'PL'},
                      # {'label': 'PT', 'value': 'PT'},
                      # {'label': 'NL', 'value': 'NL'},
                        {'label': '---', 'value': '---'}
                      # {'label': 'RO', 'value': 'RO'},
                      # {'label': 'GB', 'value': 'GB'},
                      # {'label': 'LK', 'value': 'LK'},
                      # {'label': 'CH', 'value': 'CH'},
                      # {'label': 'TW', 'value': 'TW'},
                      # {'label': 'CZ', 'value': 'CZ'},
                      # {'label': 'TN', 'value': 'TN'},
                      # {'label': 'TR', 'value': 'TR'},
                      # {'label': 'VN', 'value': 'VN'}                      
                    ],
                    value='---',
                    className='form-control'
                ),
                dbc.Tooltip(
                    info_countryDyeing_content,
                    target="countryDyeing",
                    placement="right",
                    trigger="click hover",
                    className='custom-tooltip'  # Appliquer la classe CSS personnalisée  
                )
            ], className='mb-3'),
            
            html.Div([
                html.Label("Country Making, (Code pays pour l'étape de Confection)", className='form-label'),
                # dcc.Input(id='countryMaking', type='text', value='---', className='form-control'),
                dcc.Dropdown(
                    id='countryMaking',
                    options=[
                      # {'label': 'RAF', 'value': 'RAF'},
                      # {'label': 'AL', 'value': 'AL'},
                      # {'label': 'DE', 'value': 'DE'},
                      # {'label': 'RNA', 'value': 'RNA'},
                      # {'label': 'RLA', 'value': 'RLA'},
                        {'label': 'RAS', 'value': 'RAS'},
                      # {'label': 'BD', 'value': 'BD'},
                      # {'label': 'BE', 'value': 'BE'},
                      # {'label': 'KH', 'value': 'KH'},
                        {'label': 'CN', 'value': 'CN'},
                      # {'label': 'EG', 'value': 'EG'},
                      # {'label': 'ES', 'value': 'ES'},
                      # {'label': 'ET', 'value': 'ET'},
                      # {'label': "REE", 'value': "REE"},
                      # {'label': "REO", 'value': "REO"},
                        {'label': 'FR', 'value': 'FR'},
                      # {'label': 'GR', 'value': 'GR'},
                      # {'label': 'HU', 'value': 'HU'},
                      # {'label': 'IN', 'value': 'IN'},
                      # {'label': 'IT', 'value': 'IT'},
                      # {'label': 'MA', 'value': 'MA'},
                      # {'label': 'RME', 'value': 'RME'},
                      # {'label': 'MM', 'value': 'MM'},
                      # {'label': 'ROC', 'value': 'ROC'},
                        {'label': 'PK', 'value': 'PK'},
                      # {'label': 'PL', 'value': 'PL'},
                      # {'label': 'PT', 'value': 'PT'},
                      # {'label': 'NL', 'value': 'NL'},
                        {'label': '---', 'value': '---'}
                      # {'label': 'RO', 'value': 'RO'},
                      # {'label': 'GB', 'value': 'GB'},
                      # {'label': 'LK', 'value': 'LK'},
                      # {'label': 'CH', 'value': 'CH'},
                      # {'label': 'TW', 'value': 'TW'},
                      # {'label': 'CZ', 'value': 'CZ'},
                      # {'label': 'TN', 'value': 'TN'},
                      # {'label': 'TR', 'value': 'TR'},
                      # {'label': 'VN', 'value': 'VN'}                      
                    ],
                    value='---',
                    className='form-control'
                ),
                dbc.Tooltip(
                    info_countryMaking_content,
                    target="countryMaking",
                    placement="right",
                    trigger="click hover",
                    className='custom-tooltip'  # Appliquer la classe CSS personnalisée  
                )
            ], className='mb-3'),
            
            html.Div([
                html.Label("Air Transport Ratio (Min 0 | Max 1. Part de transport aérien entre l'étape de Confection et l'étape de Distribution)", className='form-label'),
                dcc.Input(id='airTransportRatio', type='number', value=1.0, min=0, max=1, step=0.01, className='form-control'),
            ], className='mb-3'),
            
            html.Div([
                html.Label("Business, (Type d'entreprise et d'offre de services)", className='form-label'),
                dcc.Dropdown(
                    id='business',
                    options=[
                        {'label': 'Small Business', 'value': 'small-business'},
                        {'label': 'Large Business with Services', 'value': 'large-business-with-services'},
                        {'label': 'Large Business without Services', 'value': 'large-business-without-services'}
                    ],
                    value='large-business-without-services',
                    className='form-control'
                ),
            ], className='mb-3'),
            
            html.Div([
                html.Label("Number of References (Min 1 | Max 999999. Nombre de références au catalogue de la marque)", className='form-label'),
                dcc.Input(id='numberOfReferences', type='number', value=100000, min=1, max=999999, step=1, className='form-control'),
            ], className='mb-3'),
            
            html.Div([
                html.Label("Price (Min 15€ | Max 50€. Prix du produit, en Euros)", className='form-label'),
                dcc.Input(id='price', type='number', value=15.0, min=15.0, max=50.0, step=1.0, className='form-control'),
            ], className='mb-3'),
            
            html.Div([
                html.Label("Traceability, (Traçabilité renforcée)", className='form-label'),
                dcc.Dropdown(
                    id='traceability',
                    options=[
                        {'label': 'True', 'value': 'True'},
                        {'label': 'False', 'value': 'False'}
                    ],
                    value='False',
                    className='form-control'
                ),
            ], className='mb-3'),
            
            html.Button('Prédire', id='predict-button', n_clicks=0, className='btn btn-primary mt-3', disabled=True),
            html.Div(id='error-message', className='text-danger mt-3')
        ], className='container'),
        
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Prédiction de l'écoscore")),
            dbc.ModalBody(id='prediction-output'),
            dbc.ModalFooter(
                dbc.Button("Fermer", id="close", className="ms-auto", n_clicks=0)
            ),
        ], id="modal", is_open=False),        

    ], className='container', style={'background': 'beige', 'padding': '20px'})


def update_fields(mode, pays):
    ctx = dash.callback_context
    if not ctx.triggered:
        return no_update, no_update, no_update, no_update, no_update
    input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if input_id == 'mode':
        if mode == 'Majorant par defaut':
            return 'Pays inconnu', '---', '---', '---', '---'
        if mode == 'Mode ethique':
            return 'France', 'CN', 'FR', 'FR', 'FR'
        if mode == 'Mode fast fashion':
            return 'Chine', 'CN', 'CN', 'CN', 'CN'
        if mode == 'Mode ultra fast fashion':
            return 'Asie', 'RAS', 'RAS', 'RAS', 'RAS'
        if mode == 'Mode traditionnelle':
            return 'France', 'TR', 'FR', 'FR', 'FR'
    elif input_id == 'pays':
        if pays == 'Pays inconnu':
            return no_update, '---', '---', '---', '---'
        if pays == 'Asie':
            return no_update, 'RAS', 'RAS', 'RAS', 'RAS'
        if pays == 'Chine':
            return no_update, 'CN', 'CN', 'CN', 'CN'
        if pays == 'France':
            return no_update, 'FR', 'FR', 'FR', 'FR'
        if pays == 'Pakistan':
            return no_update, 'PK', 'PK', 'PK', 'PK'
    return no_update, no_update, no_update, no_update, no_update


def predict_ecoscore(n_clicks_predict, n_clicks_close, libelle, masse, matiere, mode, pays, product, countrySpinning, countryFabric, countryDyeing, countryMaking, airTransportRatio, business, numberOfReferences, price, traceability, is_open):
    if n_clicks_predict > 0:
        # Validation des champs
        if airTransportRatio is None or not (0 <= airTransportRatio <= 1):
            return is_open, "", "Saisie erronée : airTransportRatio. Vérifiez vos paramètres."
        if price is None or not (1.0 <= price <= 1000.0):
            return is_open, "", "Saisie erronée : price. Vérifiez vos paramètres."
        if numberOfReferences is None or not (1 <= numberOfReferences <= 999999):
            return is_open, "", "Saisie erronée : numberOfReferences. Vérifiez vos paramètres."
        
        # Convertir la valeur de traceability en 0 ou 1
        traceability_int = 1 if traceability == 'True' else 0
        
        new_data = {
            'Libelle': libelle,
            'Masse': masse,
            'Matiere': matiere,
            'Mode': mode,
            'Pays': pays,
            'product': product,
            'countrySpinning': countrySpinning,
            'countryFabric': countryFabric,
            'countryDyeing': countryDyeing,
            'countryMaking': countryMaking,
            'airTransportRatio': airTransportRatio,
            'business': business,
            'numberOfReferences': numberOfReferences,
            'price': price,
            'traceability': traceability_int
        }
        
        df_new = pd.DataFrame([new_data])
        df_new = df_new[['Pays', 'Masse', 'Mode', 'Matiere', 'business', 'numberOfReferences', 'price', 'traceability', 'product', 'airTransportRatio', 'countrySpinning', 'countryFabric', 'countryDyeing', 'countryMaking']]
        
        y_pred_new = pipeline_loaded.predict(df_new)
        y_pred_new_rounded = round(y_pred_new[0])
        
        if y_pred_new_rounded >= 0:
            prediction_message = html.Div(
                f"Prédiction de l'ecoscore 'ecs' pour ces nouvelles données saisies : {y_pred_new_rounded} Pts",
                style={'color': 'green'}
            )
        else:
            prediction_message = html.Div([
                "Attention. Ecoscore 'ecs' négatif !! Vérifiez la cohérence des paramètres saisis.",
                html.Br(),
                f"Prédiction de l'ecoscore 'ecs' pour ces nouvelles données saisies : {y_pred_new_rounded} Pts"
            ], style={'color': 'red'})
        
        return not is_open, prediction_message, ""
    
    if n_clicks_close > 0:
        return not is_open, "", ""
    
    return is_open, "", ""
