# components.py
from dash import html, dcc

# composant(s) réutilisable(s) 
def create_header(title):
    return html.H1(title, style={'textAlign': 'center'})

def create_footer():
    return html.Footer("© Nov. 2024, DataScientest - Projet Ecobalyse - GitHub : https://github.com/dte-thierry/prj_ECOBALYSE", 
                       style={'textAlign': 'center', 'padding': '10px'})

def create_message(lines, style=None):
    # Joindre les lignes avec des sauts de ligne explicites
    message = "  \n".join(lines)
    return html.Div([
        dcc.Markdown(message, style=style)
    ], style={'whiteSpace': 'pre-line'})

