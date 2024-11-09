# page10.py - menu Visualisation(s), liste des requetes 
from dash import html, dcc

from components import create_header, create_footer, create_message

# Créer la mise en page de la page 10
def create_page10_layout():
    queries = [
        "Listing & Description des Données",
        "Nombre de Textiles par Catégories",
        "Distribution cumulée de l'ecoscore 'ecs' par Catégories de Textiles",
        "Densité estimée & répartition cumulée de la variable 'ecs'",
        "Boxplot : mode / ecs",
        "Boxplot : pays / ecs"                
    ]

    return html.Div([
        create_header("Visualisation(s) des Données Textiles"),
        create_message(["---"], style={'fontSize': 20}),
        create_message([
                "Le menu ci-dessous propose de visualiser les données recueillies, depuis le site [Ecobalyse](https://ecobalyse.beta.gouv.fr/#/explore/textile).",
                "Il permet aux utilisateurs d'explorer les impacts environnementaux des différents produits."
              ], style={'fontSize': 20}),
        create_message(["---"], style={'fontSize': 20}),
        html.Ul([
            html.Li(dcc.Link(query, href=f'/page-{index+11}')) for index, query in enumerate(queries)
        ], style={'fontSize': 20}),
        html.Br(),  # Ajoutez un espace avant le bouton de retour
        html.Button(
            dcc.Link('Retour', href='/'),  # Ajoutez ce bouton pour revenir à la page d'accueil
            style={'fontSize': 20, 'margin': '10px'}
        ),
        create_footer()
    ], style={'background': 'beige', 'padding': '20px'})