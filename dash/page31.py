from dash import html, dcc, callback, Input, Output, State
import dash
import pandas as pd
import joblib

import dash_bootstrap_components as dbc

# Charger le modèle
pipeline_loaded = joblib.load('linear_regression_model.pkl')

# Lire le contenu des fichiers d'informations paramètres
with open('./assets/info_masse.txt', 'r') as file:
    info_masse_content = file.read()
with open('./assets/info_matiere.txt', 'r') as file:
    info_matiere_content = file.read()
with open('./assets/info_mode.txt', 'r') as file:
    info_mode_content = file.read()


# Créer la mise en page de la page 31
def create_page31_layout():
    return html.Div([
        html.H1("Prédiction d'ecoscore 'ecs', pour la catégorie : Tshirt / Polo", className='text-center my-4'),
        
        html.Div([
            html.Div([
                html.Label('Libelle', className='form-label'),
                dcc.Input(id='libelle', type='text', value='Tshirt coton 150g Majorant par defaut', className='form-control'),
            ], className='mb-3'),
            
            html.Div([ 
                html.Label('Masse (en kg. Min 0.06 | Max 0.15)', className='form-label'),
                dcc.Input(id='masse', type='number', value=0.15, min=0.06, max=0.15, step=0.01, className='form-control'),
                dbc.Tooltip(
                    info_masse_content,
                    target="masse",
                    placement="right",
                    trigger="click hover",
                    className='custom-tooltip'  # Appliquer la classe CSS personnalisée  
                )
            ], className='mb-3'),
            
            html.Div([
                html.Label('Matiere', className='form-label'),
                dcc.Input(id='matiere', type='text', value='coton', className='form-control'),
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
                dcc.Input(id='mode', type='text', value='Majorant par defaut', className='form-control'),
                dbc.Tooltip(
                    info_mode_content,
                    target="mode",
                    placement="right",
                    trigger="click hover",
                    className='custom-tooltip'  # Appliquer la classe CSS personnalisée  
                )
            ], className='mb-3'),
            
            html.Div([
                html.Label('Pays', className='form-label'),
                dcc.Input(id='pays', type='text', value='Pays inconnu', className='form-control'),
            ], className='mb-3'),
            
            html.Div([
                html.Label('Product', className='form-label'),
                dcc.Input(id='product', type='text', value='tshirt', className='form-control', readOnly=True),
            ], className='mb-3'),
            
            html.Div([
                html.Label('Country Spinning', className='form-label'),
                dcc.Input(id='countrySpinning', type='text', value='---', className='form-control'),
            ], className='mb-3'),
            
            html.Div([
                html.Label('Country Fabric', className='form-label'),
                dcc.Input(id='countryFabric', type='text', value='---', className='form-control'),
            ], className='mb-3'),
            
            html.Div([
                html.Label('Country Dyeing', className='form-label'),
                dcc.Input(id='countryDyeing', type='text', value='---', className='form-control'),
            ], className='mb-3'),
            
            html.Div([
                html.Label('Country Making', className='form-label'),
                dcc.Input(id='countryMaking', type='text', value='---', className='form-control'),
            ], className='mb-3'),
            
            html.Div([
                html.Label('Air Transport Ratio (Min 0 | Max 1)', className='form-label'),
                dcc.Input(id='airTransportRatio', type='number', value=1.0, min=0, max=1, step=0.01, className='form-control'),
            ], className='mb-3'),
            
            html.Div([
                html.Label('Business', className='form-label'),
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
                html.Label('Number of References (Min 1 | Max 999999)', className='form-label'),
                dcc.Input(id='numberOfReferences', type='number', value=100000, min=1, max=999999, step=1, className='form-control'),
            ], className='mb-3'),
            
            html.Div([
                html.Label('Price (Min 10€ | Max 50€)', className='form-label'),
                dcc.Input(id='price', type='number', value=10.0, min=10.0, max=50.0, step=1.0, className='form-control'),
            ], className='mb-3'),
            
            html.Div([
                html.Label('Traceability', className='form-label'),
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
            
            html.Button('Prédire', id='predict-button', n_clicks=0, className='btn btn-primary mt-3'),
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

@callback(
    Output('modal', 'is_open'),
    Output('prediction-output', 'children'),
    Output('error-message', 'children'),
    Input('predict-button', 'n_clicks'),
    Input('close', 'n_clicks'),
    State('libelle', 'value'),
    State('masse', 'value'),
    State('matiere', 'value'),
    State('mode', 'value'),
    State('pays', 'value'),
    State('product', 'value'),
    State('countrySpinning', 'value'),
    State('countryFabric', 'value'),
    State('countryDyeing', 'value'),
    State('countryMaking', 'value'),
    State('airTransportRatio', 'value'),
    State('business', 'value'),
    State('numberOfReferences', 'value'),
    State('price', 'value'),
    State('traceability', 'value'),
    State('modal', 'is_open')
)

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
                f"Prédiction de l'ecoscore 'ecs' pour les nouvelles données : {y_pred_new_rounded} Pts",
                style={'color': 'green'}
            )
        else:
            prediction_message = html.Div([
                "Attention. Ecs négatif !! Vérifiez vos paramètres.",
                html.Br(),
                f"Prédiction de l'ecoscore 'ecs' pour les nouvelles données : {y_pred_new_rounded} Pts"
            ], style={'color': 'red'})
        
        return not is_open, prediction_message, ""
    
    if n_clicks_close > 0:
        return not is_open, "", ""
    
    return is_open, "", ""