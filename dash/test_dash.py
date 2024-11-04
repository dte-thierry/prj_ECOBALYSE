import os
import logging
from datetime import datetime
import dash
from dash import dcc  # import dash_core_components as dcc, is deprecated
from dash import html  # import dash_html_components as html, is deprecated

# Importer le layout de page0.py
from page0 import create_page0_layout


# Choisir des feuilles de style CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', \
                        'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialiser l'application Dash
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

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

# Définir la mise en page de l'application en utilisant le layout de page0.py
app.layout = create_page0_layout()

# Définir le point d'entrée de l'application
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)

