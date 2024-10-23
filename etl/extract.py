# Charger les librairies utiles
from utils01 import get_explorer_url
import time
import re

# Récolte des données Ecobalyse depuis : https://ecobalyse.beta.gouv.fr/#/explore/textile
url = 'https://ecobalyse.beta.gouv.fr/#/explore/textile'
columns = ['Nom', 'Categorie', 'ecs', 'pef', '.']
start = time.time()

# Lien vers la documentation
print("Les informations relatives à ces exemples de textiles sont disponibles depuis le lien :\nhttps://fabrique-numerique.gitbook.io/ecobalyse/textile/exemples\n")

# Extraire via Selenium les données de l'Explorateur [Exemples] et créer un DataFrame
print("Récupérer les données de l'Explorateur Ecobalyse ...")
df_exemples = get_explorer_url(url, columns)

# Trier le DataFrame par "Catégorie" en ordre décroissant
df_exemples = df_exemples.sort_values(by=['Categorie', 'ecs'], ascending=[False, True])

# Réinitialiser les indices du DataFrame
df_exemples = df_exemples.reset_index(drop=True)

# Supprimer les espaces de début et fin de chaîne de caractère de la colonne 'Nom'
df_exemples['Nom'] = df_exemples['Nom'].str.strip()

# Supprimer les colonnes '.' et 'pef'
df_exemples = df_exemples.drop(columns=['.'])
df_exemples = df_exemples.drop(columns=['pef'])

# Convertir la colonne 'ecs' en type : Integer
# regex : remplacer tout caractère non numérique par une chaîne vide
df_exemples['ecs'] = df_exemples['ecs'].str.replace(r'\D', '', regex=True).astype(int)

# Calculer le temps de traitement
end = time.time()
runtime = end - start

# Afficher le DataFrame
if df_exemples is not None and not df_exemples.empty:
    print(f"DataFrame créé avec succès au bout de : {runtime:.2f} secondes.")
    print(df_exemples.head())

    # Sauvegarder le DataFrame Explorateur [Exemples] en fichier JSON
    df_exemples.to_json('data/PRJ-ECOBALYSE-01-WEB_SCRAPING1_temp1.json', orient='records', lines=True)
    print("\nDataFrame sauvegardé en fichier json, avec succès.")

else:
    print("Échec de la création du DataFrame ou DataFrame vide.")