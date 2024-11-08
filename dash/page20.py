# page20.py - menu Prédiction(s), liste des textiles 
from dash import html, dcc

from components import create_header, create_footer, create_message

# Créer la mise en page de la page 20
def create_page20_layout():
    categories = [
        "Boxer / slip (tricoté)",
        "Caleçon (tissé)",
        "Chaussettes",
        "Chemise",
        "Jean",
        "Jupe / Robe",
        "Maillot de bain",
        "Manteau / Veste",
        "Pantalon",
        "Pull",
        "Tshirt / Polo"
    ]

    return html.Div([
        create_header("Prédiction(s) pour les catégories de textiles"),
        create_message(["---"], style={'fontSize': 20}),
        create_message([
                "Pour chaque catégorie, le modèle utilisé de *prédiction en Machine Learning* est : **la régression linéaire**.",
                "Les paramètres à saisir, pour de nouvelles données textiles, sont : ",
                "*Masse, Matière, Mode, Pays, countrySpinning, countryFabric, countryDyeing, countryMaking, airTransportRatio, business, numberOfReferences, price, traceability*.",
                "La variable estimée par prédiction *(indépendamment d'un calcul via l'API Ecobalyse)* est **l'écoscore global ('ecs') des impacts environnementaux**."
            ], style={'fontSize': 20}),
        create_message(["---"], style={'fontSize': 20}),
        html.Ul([
            html.Li(dcc.Link(category, href=f'/page-{index+21}')) for index, category in enumerate(categories)
        ], style={'fontSize': 20}),
        html.Br(),  # Ajoutez un espace avant le bouton de retour
        html.Button(
            dcc.Link('Retour', href='/'),  # Ajoutez ce bouton pour revenir à la page d'accueil
            style={'fontSize': 20, 'margin': '10px'}
        ),
        create_footer()
    ], style={'background': 'beige', 'padding': '20px'})