# Importer les bibliothèques nécessaires
from dash import html, dcc

from components import create_header, create_footer

# créer le 'layout' de la page d'accueil - page 0 -
def create_page0_layout():
    return html.Div([
        html.H1(
            'Dashboard EcoBalyse', 
            style={'color' : 'mediumturquoise', 'textAlign': 'center', 'fontSize': 40}
        ),

        html.Div(
            html.A(
                id="link1",
                children="(visiter le site EcoBalyse)",
                href="https://ecobalyse.beta.gouv.fr/#/",
                target="_blank",
                style={'color': 'blue', 'fontSize': 30}
            ),
            style={'textAlign': 'center'}
        ),

        # Ajouter une balise div et un paragraphe d'information
        html.H2('A propos ...', style={'color': 'mediumturquoise', 'fontSize': 35}),

        html.Br(), 

        html.Div([
            html.P([
                html.H3('Textiles & Environnement', style={'fontSize': 25}), html.Br(),
                "L'industrie textile est l'une des plus polluantes au monde ", html.Sup('1 , 2 , 3 , 4 , 5'), ".", html.Br(),
                "En lien avec les préoccupations actuelles, et sur la base d'",
                html.A(id="link2", children="Écobalyse", href="https://ecobalyse.beta.gouv.fr/", target="_blank", style={'color': 'blue'}),
                ", cet outil propose un comparatif de coûts environnementaux, en vue de favoriser un modèle de production plus durable, ", 
                "et de fournir des recommandations, ou des conseils, sur la manière de réduire l'impact écologique de textiles courants.", html.Br(), 
                html.Code("En savoir plus : "), html.Br(),
                html.Sup('1'), html.A(id="sup1", children="la-goose.com", href="https://la-goose.com/les-impacts-environnementaux-du-textile-comment-les-reduire/", target="_blank", style={'color': 'blue'}), ", ",
                html.Sup('2'), html.A(id="sup2", children="oxfamfrance.org", href="https://www.oxfamfrance.org/agir-oxfam/impact-de-la-mode-consequences-sociales-environnementales/", target="_blank", style={'color': 'blue'}), ", ",
                html.Sup('3'), html.A(id="sup3", children="ecologie.gouv.fr", href="https://www.ecologie.gouv.fr/mieux-informer-consommateur-vers-affichage-environnemental-des-vetements-indiquer-leur-impact", target="_blank", style={'color': 'blue'}), ", ",
                html.Sup('4'), html.A(id="sup4", children="climateseed.com", href="https://climateseed.com/fr/blog/secteur-du-textile-impact-environnemental-et-r%C3%A9glementation", target="_blank", style={'color': 'blue'}), ", ",
                html.Sup('5'), html.A(id="sup5", children="wwf.ch", href="https://www.wwf.ch/fr/nos-objectifs/rapport-du-wwf-sur-lindustrie-de-lhabillement-et-des-textiles", target="_blank", style={'color': 'blue'}), ", "
            ], style={'fontSize': 20})  
        ], style={'fontSize': 25}),  

        # Ajouter une image centrée
        html.Div(
            html.Img(src='/assets/page0.jpg', style={'width': '35%', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'}),
            style={'textAlign': 'center'}
        ),

        html.Br(),

        html.Div([
            html.Button(
                dcc.Link('Visualisation(s)', 
                         href='/page-1', style={'fontSize': 15})
            ),
        
            html.Button(
                dcc.Link('Prédiction(s)', 
                         href='/page-2', style={'fontSize': 15})
            )
        ], style={'display': 'flex', 'justify-content': 'center', 'gap': '2em'}),
        create_footer(),
    ], style={'background' : 'beige', 'alignItems': 'center'})