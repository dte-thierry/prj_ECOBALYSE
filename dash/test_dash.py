import os
import logging
from datetime import datetime

import dash
from dash import dcc  # import dash_core_components as dcc, is deprecated
from dash import html  # import dash_html_components as html, is deprecated
from dash.dependencies import Input, Output, State
from dash import no_update

import redis
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

# Importer le(s) layout(s) de page(s)
from page0 import create_page0_layout
from page20 import create_page20_layout
from page10 import create_page10_layout
import page31, page30, page29, page28, page27, page26, page25, page24, page23, page22, page21
import page16, page15, page14, page13, page12, page11

# Choisir des feuilles de style CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', \
                        'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

logging.basicConfig(level=logging.DEBUG)

# Initialiser la connexion Redis
r = redis.Redis(host='ecblredis', port=6379, decode_responses=True, health_check_interval=30)
print("test_dash : Redis fonctionne et le fichier JSON est bien récupéré : ", r.ping())

# Initialiser l'application Dash
logging.debug("Avant l'initialisation de l'application Dash")
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
logging.debug("Après l'initialisation de l'application Dash")

# Enregistrer les pages après l'instanciation de l'application
dash.register_page('page30', path='/page-30')
dash.register_page('page31', path='/page-31')

dash.register_page('page20', path='/page-2')
dash.register_page('page29', path='/page-29')
dash.register_page('page28', path='/page-28')
dash.register_page('page27', path='/page-27')
dash.register_page('page26', path='/page-26')
dash.register_page('page25', path='/page-25')
dash.register_page('page24', path='/page-24')
dash.register_page('page23', path='/page-23')
dash.register_page('page22', path='/page-22')
dash.register_page('page21', path='/page-21')

dash.register_page('page10', path='/page-1')
dash.register_page('page16', path='/page-16')
dash.register_page('page15', path='/page-15')
dash.register_page('page14', path='/page-14')
dash.register_page('page13', path='/page-13')
dash.register_page('page12', path='/page-12')
dash.register_page('page11', path='/page-11')

# Récupérer la variable d'environnement
dash_log_namefile = os.getenv('DASH_LOG_NAMEFILE', 'default_log_name')

# Configuration du logging
if not app.server.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    log_filename = f"logs/{dash_log_namefile}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Application Dash active.")

# Définir la mise en page de l'application 
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    
    if pathname.startswith('/page-2'):
        if pathname == '/page-2':
            return create_page20_layout()
        elif pathname == '/page-21':
            return page21.create_page21_layout()
        elif pathname == '/page-22':
            return page22.create_page22_layout()
        elif pathname == '/page-23':
            return page23.create_page23_layout()
        elif pathname == '/page-24':
            return page24.create_page24_layout()
        elif pathname == '/page-25':
            return page25.create_page25_layout()
        elif pathname == '/page-26':
            return page26.create_page26_layout()
        elif pathname == '/page-27':
            return page27.create_page27_layout()
        elif pathname == '/page-28':
            return page28.create_page28_layout()
        elif pathname == '/page-29':
            return page29.create_page29_layout()
    
    elif pathname.startswith('/page-1'):
        if pathname == '/page-1':
            return create_page10_layout()  
        elif pathname == '/page-11':
            return page11.create_page11_layout()
        elif pathname == '/page-12':
            return page12.create_page12_layout()
        elif pathname == '/page-13':
            return page13.create_page13_layout()
        elif pathname == '/page-14':
            return page14.create_page14_layout()
        elif pathname == '/page-15':
            return page15.create_page15_layout()
        elif pathname == '/page-16':
            return page16.create_page16_layout()
    
    elif pathname == '/page-30':
        return page30.create_page30_layout()
    elif pathname == '/page-31':
        return page31.create_page31_layout()
    else:
        return create_page0_layout()


@app.callback(
    Output('pays', 'value'),
    Output('countrySpinning', 'value'),
    Output('countryFabric', 'value'),
    Output('countryDyeing', 'value'),
    Output('countryMaking', 'value'),
    Input('mode', 'value'),
    Input('pays', 'value')
)
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


@app.callback(
    Output('modal', 'is_open'),
    Output('prediction-output', 'children'),
    Output('error-message', 'children'),
    Input('predict-button', 'n_clicks'),
    Input('close', 'n_clicks'),
    State('url', 'pathname'),
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
def predict_ecoscore(n_clicks_predict, n_clicks_close, pathname, libelle, masse, matiere, mode, pays, product, countrySpinning, countryFabric, countryDyeing, countryMaking, airTransportRatio, business, numberOfReferences, price, traceability, is_open):
    if pathname == '/page-31':
        return page31.predict_ecoscore(n_clicks_predict, n_clicks_close, libelle, masse, matiere, mode, pays, product, countrySpinning, countryFabric, countryDyeing, countryMaking, airTransportRatio, business, numberOfReferences, price, traceability, is_open)
    elif pathname == '/page-30':
        return page30.predict_ecoscore(n_clicks_predict, n_clicks_close, libelle, masse, matiere, mode, pays, product, countrySpinning, countryFabric, countryDyeing, countryMaking, airTransportRatio, business, numberOfReferences, price, traceability, is_open)
    elif pathname == '/page-29':
        return page29.predict_ecoscore(n_clicks_predict, n_clicks_close, libelle, masse, matiere, mode, pays, product, countrySpinning, countryFabric, countryDyeing, countryMaking, airTransportRatio, business, numberOfReferences, price, traceability, is_open)
    elif pathname == '/page-28':
        return page28.predict_ecoscore(n_clicks_predict, n_clicks_close, libelle, masse, matiere, mode, pays, product, countrySpinning, countryFabric, countryDyeing, countryMaking, airTransportRatio, business, numberOfReferences, price, traceability, is_open)
    elif pathname == '/page-27':
        return page27.predict_ecoscore(n_clicks_predict, n_clicks_close, libelle, masse, matiere, mode, pays, product, countrySpinning, countryFabric, countryDyeing, countryMaking, airTransportRatio, business, numberOfReferences, price, traceability, is_open)
    elif pathname == '/page-26':
        return page26.predict_ecoscore(n_clicks_predict, n_clicks_close, libelle, masse, matiere, mode, pays, product, countrySpinning, countryFabric, countryDyeing, countryMaking, airTransportRatio, business, numberOfReferences, price, traceability, is_open)
    elif pathname == '/page-25':
        return page25.predict_ecoscore(n_clicks_predict, n_clicks_close, libelle, masse, matiere, mode, pays, product, countrySpinning, countryFabric, countryDyeing, countryMaking, airTransportRatio, business, numberOfReferences, price, traceability, is_open)
    elif pathname == '/page-24':
        return page24.predict_ecoscore(n_clicks_predict, n_clicks_close, libelle, masse, matiere, mode, pays, product, countrySpinning, countryFabric, countryDyeing, countryMaking, airTransportRatio, business, numberOfReferences, price, traceability, is_open)
    elif pathname == '/page-23':
        return page23.predict_ecoscore(n_clicks_predict, n_clicks_close, libelle, masse, matiere, mode, pays, product, countrySpinning, countryFabric, countryDyeing, countryMaking, airTransportRatio, business, numberOfReferences, price, traceability, is_open)
    elif pathname == '/page-22':
        return page22.predict_ecoscore(n_clicks_predict, n_clicks_close, libelle, masse, matiere, mode, pays, product, countrySpinning, countryFabric, countryDyeing, countryMaking, airTransportRatio, business, numberOfReferences, price, traceability, is_open)
    elif pathname == '/page-21':
        return page21.predict_ecoscore(n_clicks_predict, n_clicks_close, libelle, masse, matiere, mode, pays, product, countrySpinning, countryFabric, countryDyeing, countryMaking, airTransportRatio, business, numberOfReferences, price, traceability, is_open)

    return is_open, "", ""

# Définir les callbacks pour les pages spécifiques
@app.callback(
    Output('density-graph', 'figure'),
    [Input('url', 'pathname')]
)
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


@app.callback(
    [Output('density-graph-14', 'figure'),
     Output('ecdf-graph', 'figure')],
    [Input('url', 'pathname')]
)
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


# Définir le point d'entrée de l'application
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)

