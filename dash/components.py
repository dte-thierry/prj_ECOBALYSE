# components.py
from dash import html, dcc
import plotly.express as px

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

# mettre à jour un boxplot
def create_boxplot(df, x_col, y_col, title, x_label, y_label):
    fig = px.box(df, x=x_col, y=y_col, points="all", color=x_col,
                 title=title,
                 labels={x_col: x_label, y_col: y_label},
                 template='plotly_white')
    return fig