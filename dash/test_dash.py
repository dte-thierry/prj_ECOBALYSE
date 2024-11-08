import os
import logging
from datetime import datetime

import dash
from dash import dcc  # import dash_core_components as dcc, is deprecated
from dash import html  # import dash_html_components as html, is deprecated
from dash.dependencies import Input, Output, State

from dash import no_update

# Importer le(s) layout(s) de page(s)
from page0 import create_page0_layout
from page20 import create_page20_layout
import page31, page30, page29, page28, page27, page26, page25, page24, page23, page22, page21

# Choisir des feuilles de style CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', \
                        'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialiser l'application Dash
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

# Enregistrer les pages après l'instanciation de l'application
dash.register_page('page20', path='/page-2')
dash.register_page('page31', path='/page-31')
dash.register_page('page30', path='/page-30')
dash.register_page('page29', path='/page-29')
dash.register_page('page28', path='/page-28')
dash.register_page('page27', path='/page-27')
dash.register_page('page26', path='/page-26')
dash.register_page('page25', path='/page-25')
dash.register_page('page24', path='/page-24')
dash.register_page('page23', path='/page-23')
dash.register_page('page22', path='/page-22')
dash.register_page('page21', path='/page-21')

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
    if pathname == '/page-2':
        return create_page20_layout()
    elif pathname == '/page-31':
        return page31.create_page31_layout()
    elif pathname == '/page-30':
        return page30.create_page30_layout()
    elif pathname == '/page-29':
        return page29.create_page29_layout()
    elif pathname == '/page-28':
        return page28.create_page28_layout()
    elif pathname == '/page-27':
        return page27.create_page27_layout()
    elif pathname == '/page-26':
        return page26.create_page26_layout()
    elif pathname == '/page-25':
        return page25.create_page25_layout()
    elif pathname == '/page-24':
        return page24.create_page24_layout()
    elif pathname == '/page-23':
        return page23.create_page23_layout()
    elif pathname == '/page-22':
        return page22.create_page22_layout()
    elif pathname == '/page-21':
        return page21.create_page21_layout()
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

# Définir le point d'entrée de l'application
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)

