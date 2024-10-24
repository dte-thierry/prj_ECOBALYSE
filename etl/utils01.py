def get_explorer_url(url, columns):
    """
    Récupère les données d'une table HTML à partir d'une URL donnée et les retourne sous forme de DataFrame.

    Paramètres:
    -----------
    url : str
        L'URL de la page web contenant la table HTML à scraper.
    columns : list
        Une liste de chaînes de caractères représentant les noms des colonnes pour le DataFrame retourné.

    Retourne:
    ---------
    pandas.DataFrame
        Un DataFrame contenant les données de la table HTML avec les colonnes spécifiées.

    Notes:
    ------
    - La fonction utilise Selenium pour automatiser le navigateur Chrome.
    - Les options du navigateur sont configurées pour désactiver les infobars, extensions et notifications.
    - Le navigateur est exécuté en mode sans tête pour éviter l'ouverture d'une fenêtre graphique.
    - Les capacités SSL sont acceptées pour gérer les certificats sécurisés et non sécurisés.
    - La fonction attend jusqu'à 10 secondes pour que la page se charge complètement avant de scraper les données.
    - Le DataFrame retourné aura les colonnes nommées selon la liste fournie en paramètre.
    """
    # Charger les librairies nécessaires
    import pandas as pd
    import os

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service

    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    
    # Définir les capacités
    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['acceptSslCerts'] = True 
    capabilities['acceptInsecureCerts'] = True

    # Ajouter les capacités aux options
    options = Options()
    options.add_argument("--disable-infobars")  # Désactiver les fenêtres contextuelles
    options.add_argument("--disable-extensions")  # Désactiver les extensions
    options.add_argument("--disable-notifications")  # Désactiver les notifications
    options.add_experimental_option('prefs', {'profile.default_content_setting_values.notifications': 2}) # Désactiver les notifications
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")  # Exécuter en mode sans tête    
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    # Ajouter les capacités aux options
    options.add_experimental_option('prefs', capabilities)

    # Vérifier si le script est exécuté dans un conteneur Docker
    if os.path.exists('/.dockerenv'):
        # Spécifier le chemin de l'exécutable ChromeDriver / conteneur
        chrome_service = Service('/usr/bin/chromedriver')
    else:
        # Spécifier le chemin de l'exécutable ChromeDriver / manuel
        chrome_service = Service('/usr/bin/chromedriver')

    # Créer une nouvelle instance de navigateur avec des options et le service
    driver = webdriver.Chrome(service=chrome_service, options=options)
    
    # Rechercher la page à afficher 
    driver.get(url)
    
    # Attendre que la page se charge
    wait = WebDriverWait(driver, 10)
    
    # Extraire les données find_elements(By.CSS_SELECTOR, 'table tr')
    # Sélecteur CSS pour les lignes du tableau
    data = []
    rows = driver.find_elements(By.CSS_SELECTOR, 'table tr') 
    
    # Sélecteur CSS pour les colonnes du tableau
    for row in rows:
        cols = row.find_elements(By.CSS_SELECTOR, 'td')  
        cols = [col.text for col in cols]
        data.append(cols)
    
    # Fermer le webdriver
    driver.close()

    # Créer le dataframe
    df = pd.DataFrame(data)
    
    # Nommer les colonnes
    df.columns = columns
    
    return df


def diviser_nom(ligne):
    """
    Divise une chaîne de caractères représentant un nom en plusieurs éléments distincts.

    Cette fonction prend une chaîne de caractères contenant des informations séparées par des tirets
    et les divise en trois parties : le type, le pays et le mode. Elle traite également les cas où
    le pays est indiqué comme "Majorant par défaut" ou "Remanufacturé".

    Paramètres :
    -----------
    ligne : str
        La chaîne de caractères à diviser. Elle est supposée contenir des informations séparées par des tirets.

    Retour :
    --------
    pandas.Series
        Une série contenant trois éléments : le type, le pays et le mode.
    """
    # Charger les librairies nécessaires
    import pandas as pd
    
    elements = ligne.rsplit('-', maxsplit=3)  # Divise la chaîne en partant de la droite
    elements = [e.strip() for e in elements]  # Supprime les espaces superflus
    # Assignation des éléments aux colonnes en tenant compte de l'ordre inverse
    type = elements[0]
    mode = elements[-1]
    # Remplacer "Majorant par défaut" et "Remanufacturé" par "Pays inconnu"
    if elements[1] in ["Majorant par défaut", "Remanufacturé"]:
        elements[1] = "Pays inconnu"
    pays = elements[1]
    
    return pd.Series([type, pays, mode])


def extraire_masse(type):
    """
    Extrait la masse d'une chaîne de caractères et la convertit en kilogrammes.

    Cette fonction utilise une expression régulière pour rechercher une masse exprimée en grammes
    entre parenthèses dans une chaîne de caractères. Si une masse est trouvée, elle est convertie
    en kilogrammes et retournée. Sinon, la fonction retourne None.

    Paramètres :
    -----------
    type : str
        La chaîne de caractères contenant potentiellement une masse entre parenthèses, suivie de 'g'.

    Retour :
    --------
    float or None
        La masse en kilogrammes si elle est trouvée, sinon None.
    """
    # Charger les librairies utiles
    import re

    # Utiliser une expression régulière pour trouver la masse entre parenthèses
    mass = re.search(r'\((.*?)g\)', type)
    # Si une masse est trouvée, la retourner en tant que float
    if mass:
        return float(mass.group(1))/1000
    # Si aucune masse n'est trouvée, retourner None
    return None


def extraire_matiere(type_colonne):
    """
    Extrait la matière d'une chaîne de caractères représentant un type de produit.

    Cette fonction utilise une expression régulière pour rechercher des matières spécifiques dans une chaîne de caractères.
    Si une matière est trouvée, elle est retournée. Sinon, une chaîne vide est retournée.

    Paramètres :
    -----------
    type_colonne : str
        La chaîne de caractères contenant le type de produit.

    Retour :
    --------
    str
        La matière trouvée dans la chaîne de caractères, ou une chaîne vide si aucune matière n'est trouvée.
    """
    # Charger les librairies utiles
    import re

    # Liste des matières possibles. Attention : faute d'orthographe pour 'paysane' au lieu de 'paysanne' !
    matieres = ['laine paysane', 'synthétique', 'coton bio', 'polyester', 'viscose', 'laine', 'coton', 'lin']

    # Créer une expression régulière à partir de la liste des matières
    pattern = r'\b(' + '|'.join(re.escape(matiere) for matiere in matieres) + r')\b'

    # Vérifier si 'laine paysane' est dans la chaîne
    if 'laine paysane' in type_colonne:
        return 'laine paysane'
    
    # Rechercher les autres matières
    match = re.search(pattern, type_colonne)
    if match:
        return match.group(0)
    
    return ''


def get_ecobalyse_datas(url, columns, json_output_path):
    """
    Récupère et traite les données de l'Explorateur Ecobalyse, puis les sauvegarde en fichier JSON.

    Parameters:
    url (str): L'URL de l'Explorateur Ecobalyse.
    columns (list): Liste des colonnes à extraire.
    json_output_path (str): Chemin du fichier JSON où sauvegarder les données.

    Returns:
    pd.DataFrame: Le DataFrame contenant les données traitées.

    Description:
    Cette fonction utilise Selenium pour extraire les données de l'Explorateur Ecobalyse à partir de l'URL fournie.
    Les données sont ensuite traitées pour :
    - Trier par catégorie et ECS.
    - Réinitialiser les indices.
    - Supprimer les espaces en début et fin de chaîne dans la colonne 'Nom'.
    - Supprimer les colonnes inutiles.
    - Convertir la colonne 'ecs' en type entier.
    - Diviser les informations de la colonne 'Nom' en plusieurs colonnes.
    - Extraire la masse et la matière des colonnes correspondantes.
    - Renommer et réorganiser les colonnes.
    Le DataFrame résultant est sauvegardé en fichier JSON et retourné.
    """
    # Charger les librairies utiles
    import pandas as pd
    import time
    import re
    
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

    # Diviser les informations de la colonne 'Nom'
    df_exemples[['Type', 'Pays', 'Mode']] = df_exemples['Nom'].apply(diviser_nom)

    # Récupérer la masse depuis la colonne 'Type'
    df_exemples['Masse'] = df_exemples['Type'].apply(extraire_masse)

    # Supprimer la masse de la colonne 'Type'
    df_exemples['Type'] = df_exemples['Type'].apply(lambda x: re.sub(r'\(.*?g\)', '', x).strip())

    # Récupérer la matière depuis la colonne 'Type'
    df_exemples['Matiere'] = df_exemples['Type'].apply(extraire_matiere)

    # Supprimer la colonne 'Type'
    df_exemples = df_exemples.drop(columns=['Type'])

    # Renommer la colonne 'Nom' en 'Libelle'
    df_exemples = df_exemples.rename(columns={'Nom': 'Libelle'})

    # Calculer le temps de traitement
    end = time.time()
    runtime = end - start

    # Afficher le DataFrame
    if df_exemples is not None and not df_exemples.empty:
        print(f"DataFrame créé avec succès au bout de : {runtime:.2f} secondes.")
        
        # Afficher toutes les colonnes
        pd.set_option('display.max_columns', None)    
        print(df_exemples.head(7))
        
        # Sauvegarder le DataFrame Explorateur [Exemples] en fichier JSON
        df_exemples.to_json(json_output_path, orient='records', lines=True)
        print("\nDataFrame sauvegardé en fichier json, avec succès.\n")
        
    else:
        print("\nÉchec de la création du DataFrame ou DataFrame vide.")
    
    return df_exemples
