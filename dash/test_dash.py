import os
import logging
from datetime import datetime
import dash
from dash import dcc  # import dash_core_components as dcc, is deprecated
from dash import html  # import dash_html_components as html, is deprecated

# Initialiser l'application Dash
app = dash.Dash(__name__)

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
app.layout = html.Div(children=[
    html.H1(children='Dash'),

    html.Div(children='''
        Bienvenue sur la page d'accueil de votre application Dash !
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3, 4, 5], 'y': [4, 1, 3, 5, 2], 'type': 'line', 'name': 'SF'},
                {'x': [1, 2, 3, 4, 5], 'y': [2, 4, 5, 3, 1], 'type': 'bar', 'name': 'NYC'},
            ],
            'layout': {
                'title': 'Exemple de Visualisation de Données'
            }
        }
    )
])

# Définir le point d'entrée de l'application
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
