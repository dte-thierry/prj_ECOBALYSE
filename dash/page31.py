from dash import html, dcc, callback, Input, Output, State
import dash
import pandas as pd
import joblib

# Charger le modèle
pipeline_loaded = joblib.load('linear_regression_model.pkl')

# Créer la mise en page de la page 31
def create_page31_layout():
    return html.Div([
        html.H1('Prédiction de l\'ecoscore pour Tshirt / Polo', style={'textAlign': 'center'}),
        
        html.Div([
            html.Label('Libelle'),
            dcc.Input(id='libelle', type='text', value='Tshirt coton 150g Majorant par defaut'),
            
            html.Label('Masse'),
            dcc.Input(id='masse', type='number', value=0.15),
            
            html.Label('Matiere'),
            dcc.Input(id='matiere', type='text', value='coton'),
            
            html.Label('Mode'),
            dcc.Input(id='mode', type='text', value='Majorant par defaut'),
            
            html.Label('Pays'),
            dcc.Input(id='pays', type='text', value='Pays inconnu'),
            
            html.Label('Product'),
            dcc.Input(id='product', type='text', value='tshirt'),
            
            html.Label('Country Spinning'),
            dcc.Input(id='countrySpinning', type='text', value='---'),
            
            html.Label('Country Fabric'),
            dcc.Input(id='countryFabric', type='text', value='---'),
            
            html.Label('Country Dyeing'),
            dcc.Input(id='countryDyeing', type='text', value='---'),
            
            html.Label('Country Making'),
            dcc.Input(id='countryMaking', type='text', value='---'),
            
            html.Label('Air Transport Ratio'),
            dcc.Input(id='airTransportRatio', type='number', value=1.0),
            
            html.Label('Business'),
            dcc.Input(id='business', type='text', value='large-business-without-services'),
            
            html.Label('Number of References'),
            dcc.Input(id='numberOfReferences', type='number', value=100000),
            
            html.Label('Price'),
            dcc.Input(id='price', type='number', value=10.0),
            
            html.Label('Traceability'),
            dcc.Input(id='traceability', type='text', value='False'),
            
            html.Button('Prédire', id='predict-button', n_clicks=0)
        ], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '10px'}),
        
        html.Div(id='prediction-output', style={'marginTop': '20px', 'textAlign': 'center'})
    ])

@callback(
    Output('prediction-output', 'children'),
    Input('predict-button', 'n_clicks'),
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
    State('traceability', 'value')
)
def predict_ecoscore(n_clicks, libelle, masse, matiere, mode, pays, product, countrySpinning, countryFabric, countryDyeing, countryMaking, airTransportRatio, business, numberOfReferences, price, traceability):
    if n_clicks > 0:
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
            'traceability': traceability
        }
        
        df_new = pd.DataFrame([new_data])
        df_new = df_new[['Pays', 'Masse', 'Mode', 'Matiere', 'business', 'numberOfReferences', 'price', 'traceability', 'product', 'airTransportRatio', 'countrySpinning', 'countryFabric', 'countryDyeing', 'countryMaking']]
        
        y_pred_new = pipeline_loaded.predict(df_new)
        y_pred_new_rounded = round(y_pred_new[0])
        
        return f"Prédiction de l'ecoscore 'ecs' pour les nouvelles données : {y_pred_new_rounded} Pts"
    return ""
