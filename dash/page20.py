from dash import html, dcc

from components import create_header, create_footer, create_message

# Créer la mise en page de la page 2
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
                "Les variables à saisir sont : ",
                "La variable estimée par prédiction *(indépendamment d'un calcul via l'API Ecobalyse)* est **l'écoscore ('ecs')**."
            ], style={'fontSize': 20}),
        create_message(["---"], style={'fontSize': 20}),
        html.Ul([
            html.Li(dcc.Link(category, href=f'/page-{index+21}')) for index, category in enumerate(categories)
        ], style={'fontSize': 20}),
        create_footer()
    ], style={'background': 'beige', 'padding': '20px'})