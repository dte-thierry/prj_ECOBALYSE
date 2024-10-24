def load_params_from_file(file_path):
    """
    Charge des paramètres à partir d'un fichier et les retourne sous forme de liste.

    Cette fonction lit un fichier contenant des définitions de variables, exécute le contenu du fichier
    dans un dictionnaire de paramètres, puis extrait et retourne les valeurs des variables dont les noms
    commencent par 'params'.

    Paramètres :
    -----------
    file_path : str
        Le chemin du fichier à lire. Le fichier doit contenir des définitions de variables Python.

    Retour :
    --------
    list
        Une liste contenant les valeurs des variables dont les noms commencent par 'params'.
    """
    params = {}
    with open(file_path, 'r') as file:
        exec(file.read(), params)
    return [params[key] for key in params if key.startswith('params')]


def create_textile_data(params):
    """
    Crée des données textiles en utilisant les paramètres fournis.

    Cette fonction prend un dictionnaire de paramètres et les passe à une fonction appelée `load_textile_data`
    en utilisant le déballage des arguments (**params). La fonction `load_textile_data` est supposée être définie
    ailleurs dans le code et est responsable de traiter les paramètres pour créer les données textiles.

    Paramètres :
    -----------
    params : dict
        Un dictionnaire contenant les paramètres nécessaires pour créer les données textiles. Les clés du dictionnaire
        doivent correspondre aux arguments attendus par la fonction `load_textile_data`.

    Retour :
    --------
    object
        Le résultat de l'appel à la fonction `load_textile_data` avec les paramètres fournis. Le type exact de l'objet
        retourné dépend de l'implémentation de `load_textile_data`.
    """
    return load_textile_data(**params)


def load_textile_data(libelle=None, mass=0.15, materials={'id': 'ei-coton', 'share': 1}, product='tshirt', countrySpinning=0, countryFabric='---',
                     countryDyeing='---', countryMaking='---', fabricProcess=None, airTransportRatio=1, makingWaste=None, makingDeadStock=None,
                     makingComplexity=None, yarnSize=None, surfaceMass=None, fading=None, disabledSteps=[], dyeingMedium=None, printing=None,    
                     business=None, numberOfReferences=None, price=None, traceability=None, upcycled=None, physicalDurability=None):

    """
    Paramètres nécessaires au calcul des impacts environnementaux d'un produit textile.
    Voir : https://ecobalyse.beta.gouv.fr/#/api
    
    mass :      Masse du produit fini, exprimée en kilogrammes. Min 0.01 
    materials : Liste des matières composant le produit. 
                Liste disponible sur le point d'entrée : https://ecobalyse.beta.gouv.fr/#/explore/textile/materials
                Procédé de filature ou filage pour la matière :
                https://fabrique-numerique.gitbook.io/ecobalyse/textile/cycle-de-vie-des-produits-textiles/etape-2-fabrication-du-fil
                Le format de chaque entrée est composé de l'identifiant de la matière et de la part du produit qu'elle représente, 
                optionnellement du procédé de filature ou filage pour la matière, 
                (ConventionalSpinning | UnconventionalSpinning | SyntheticSpinning) et optionnellement du code du pays d'origine
                de la matière. 
                Exemple(s) :
                ei-coton;0.3;UnconventionalSpinning;FR | ei-coton;0.3;;FR | ei-coton;0.3, coton-rdp;0.3, ei-pet;0.4 |
                ei-coton;1 | ei-coton;0.7, ei-pet;0.3 | ei-coton;0.96;UnconventionalSpinning | 
    product :   Identifiant du produit (voir : textile/products)
                Liste disponible sur le point d'entrée : https://ecobalyse.beta.gouv.fr/#/explore/textile/products
                Exemple(s) : tshirt | pantalon
    countrySpinning :
                Code pays pour l'étape de Filature
                Liste disponible sur le point d'entrée : https://ecobalyse.beta.gouv.fr/#/explore/textile/countries
                Si non spécifié, le pays de filature pris en considération est celui de production de la matière la plus représentée 
                dans le mix.
                Exemple(s) :
                0 | CN | FR
    countryFabric :
                Code pays pour l'étape de Tissage/Tricotage
                Liste disponible sur le point d'entrée : https://ecobalyse.beta.gouv.fr/#/explore/textile/countries
                Exemple(s) :
                CN | FR
    countryDyeing :
                Code pays pour l'étape de Teinture
                Liste disponible sur le point d'entrée : https://ecobalyse.beta.gouv.fr/#/explore/textile/countries
                Exemple(s) :
                CN | FR
    countryMaking : 
                Code pays pour l'étape de Confection
                Liste disponible sur le point d'entrée : https://ecobalyse.beta.gouv.fr/#/explore/textile/countries
                Exemple(s) :
                CN | FR
    fabricProcess : 
                Le processus utilisé pour tisser ou tricoter le tissu, parmi la liste de choix suivants :
                knitting-mix | knitting-fully-fashioned | knitting-integral | knitting-circular | knitting-straight | weaving
    airTransportRatio :
                Min 0 | Max 1. Part de transport aérien entre l'étape de Confection et l'étape de Distribution, entre 0 et 1
    makingWaste :
                Min 0 | Max 0.4
                Taux de perte en confection (incluant la découpe), entre 0 et 0.4
                Sur les produits tricotés en "fully fashioned / seamless", ce paramètre n'a aucun impact (valeur fixe: 0.02)
                Sur les produits tricotés en "integral / whole garment", ce paramètre n'a aucun impact (valeur fixe: 0)
    makingDeadStock :
                Min 0 | Max 0.3
                Taux de stocks dormants lors de la confection, entre 0 et 0.3
    makingComplexity :
                Complexité de la confection, parmi la liste de choix suivants :
                very-high ┃ high ┃ medium ┃ low ┃ very-low
                Sur les produits tricotés en "fully fashioned / seamless", ce paramètre n'a aucun impact (valeur fixe: very-low)
                Sur les produits tricotés en "integral / whole garment", ce paramètre n'a aucun impact (valeur fixe: vide, non applicable)
    yarnSize :  Titrage du fil exprimé en numéro métrique (Nm). 
                Il est aussi possible de l'exprimer en décitex (Dtex) en spécifiant l'unité. 
                Exemple(s) :
                40 | 40Nm | 250Dtex 
    surfaceMass :
                Min 80 | Max 500
                Le grammage de l'étoffe, exprimé en gr/m2, représente sa masse surfacique
                Sur les produits tricotés, ce paramètre n'impacte que l'impression
    fading :    Active l'application du procédé de délavage pour l'étape de confection d'un produit
                Exemple(s) :
                0 | true | false
    disabledSteps :
                Liste des étapes du cycle de vie à désactiver, séparée par des virgules. 
                Chaque étape est identifiée par un code :
                material | spinning | fabric | ennobling | making | distribution | use | eol
                Par exemple, pour désactiver l'étape de filature ainsi que celle d'ennoblissement, on peut passer :
                disabledSteps=spinning,ennobling
                Exemple(s) :
                0 | making | spinning,ennobling
    dyeingMedium :
                Ce paramètre permet de préciser le support sur lequel s'effectue la teinture.
                Il peut prendre les valeurs suivantes : article | fabric | yarn
                En l'absence d'utilisation explicite du paramètre, le support de teinture utilisé sera celui affecté par défaut 
                à la famille de produit.
                Exemple(s) :
                0 | article | fabric | yarn
    printing :  Ce paramètre permet de préciser le type d'impression effectuée sur le produit, suivi du pourcentage de surface teinte. 
                Par exemple, pigment;0.1 signifie impression pigmentaire sur 10% de la superficie du vêtement. 
                L'identifiant de procédé d'impression peut prendre les valeurs suivantes : 
                pigment | substantive
                Exemple(s) : 0 | pigment;0.5 | substantive;0.2
    business :  Type d'entreprise et d'offre de services. Choix possibles :
                small-business | large-business-with-services | large-business-without-services
    numberOfReferences : 
                Min 1 | Max 999999. Nombre de références au catalogue de la marque
    price :     Min 1 | Max 1000. Prix du produit, en Euros (€)
    traceability : 
                Traçabilité renforcée. Choix parmi : true | false
    upcycled : 
                Produit remanufacturé. Choix parmi : true | false
    physicalDurability : Min 0.67 | Max 1.45. La durabilité physique du produit  
    """
    # Paramètres d'entrées nécessaires à l'API de calcul d'impacts environnementaux des textiles
    data = {
        'libelle': libelle,
        'mass': mass,
        'materials': materials,
        'product': product,
        'countrySpinning': countrySpinning,
        'countryFabric': countryFabric,
        'countryDyeing': countryDyeing,
        'countryMaking': countryMaking,
        'fabricProcess': fabricProcess,
        'airTransportRatio': airTransportRatio,
        'makingWaste': makingWaste,           # à ajuster manuellement
        'makingDeadStock': makingDeadStock,   # à ajuster manuellement
        'makingComplexity': makingComplexity,
        'yarnSize': yarnSize,
        'surfaceMass': surfaceMass,
        'fading': fading,
        'disabledSteps': disabledSteps,      # bug API ? ex: ['use']
        'dyeingMedium': dyeingMedium,
        'printing': printing,
        'business': business,
        'numberOfReferences' : numberOfReferences,
        'price' : price,
        'traceability' : traceability,
        'upcycled' : upcycled,
        'physicalDurability' : physicalDurability
    }
    return data


def remove_dashes(input_str):
    """
    Supprime les accents, les guillemets, les parenthèses, les tirets et les espaces superflus d'une chaîne de caractères.

    Cette fonction prend une chaîne de caractères en entrée et effectue les opérations suivantes :
    1. Normalise la chaîne pour séparer les accents des caractères de base.
    2. Supprime les accents.
    3. Supprime les guillemets doubles.
    4. Supprime les parenthèses.
    5. Supprime les tirets.
    6. Supprime les espaces superflus (multiples espaces sont réduits à un seul espace).

    Paramètres :
    -----------
    input_str : str
        La chaîne de caractères à traiter.

    Retour :
    --------
    str
        La chaîne de caractères nettoyée, sans accents, guillemets, parenthèses, tirets et espaces superflus.

    Exemple :
    ---------
    Supposons que l'entrée soit :
    input_str = 'T-shirt coton (150g) - "fast fashion"'

    Appeler `remove_dashes(input_str)` retournera :
    'Tshirt coton 150g fast fashion'
    """
    # Charger les librairies utiles
    import unicodedata
    
    # Traitement pour supprimer les accents, les guillemets, les parenthèses et les tirets
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    without_accents = ''.join([c for c in nfkd_form if not unicodedata.combining(c)])
    without_quotes = without_accents.replace('"', '')
    without_parentheses = without_quotes.replace('(', '').replace(')', '')
    without_dashes = without_parentheses.replace('-', '')
    without_extra_spaces = ' '.join(without_dashes.split())
    return without_extra_spaces


def find_description(df_initial, data, api_token):
    """
    Envoie une requête à l'API Ecobalyse pour obtenir des descriptions environnementales et met à jour un DataFrame avec ces informations.

    Cette fonction prend un DataFrame initial, des données de paramètres et un jeton d'API, envoie une requête POST à l'API Ecobalyse,
    traite la réponse, et met à jour le DataFrame initial avec la description obtenue pour le libellé correspondant.

    Paramètres :
    -----------
    df_initial : pandas.DataFrame
        Le DataFrame initial contenant les informations sur les textiles. Les colonnes 'Libelle', 'Pays', 'Mode' et 'Matiere' seront nettoyées.
    
    data : dict
        Un dictionnaire contenant les paramètres nécessaires pour la requête API. Le libellé sera nettoyé avant la comparaison.
    
    api_token : str
        Le jeton d'API utilisé pour l'autorisation de la requête API.

    Retour :
    --------
    pandas.DataFrame
        Le DataFrame initial mis à jour avec la description obtenue de l'API pour le libellé correspondant.
    """
    # Charger les librairies utiles
    import requests
    import pandas as pd
    import math
    
    # URL de l'API Ecobalyse
    link = 'https://ecobalyse.beta.gouv.fr/api/'

    # Créer un dictionnaire pour les en-têtes
    headers = {
        'Authorization': 'Bearer {}'.format(api_token),
    }

    # Scrapper API avec le dictionnaire
    result2 = requests.post(link + 'textile/simulator', headers=headers, json=data) # passage des paramètres 'data'
    
    # Vérifiez le statut de la requête
    if result2.status_code == 200:
        # Convertir la réponse en JSON
        response_json = result2.json()
        
        # Supprimer les caractères spéciaux dans le DataFrame initial
        columns_to_clean = ['Libelle', 'Pays', 'Mode', 'Matiere']
        for column in columns_to_clean:
            df_initial[column] = df_initial[column].apply(remove_dashes)

        # Supprimer les accents, les guillemets, les parenthèses et les tirets du libellé dans les données
        data['libelle'] = remove_dashes(data['libelle'])        
        
        # Ajouter la description à la ligne correspondante dans le DataFrame initial
        df_initial.loc[df_initial['Libelle'] == data['libelle'], 'description'] = response_json['description']
        
        return df_initial

    else:
        print('La requête a échoué avec le code de statut ', result2.status_code, ", pour le libellé : ", data['libelle'])
        print('\nVous pouvez vérifier manuellement chacun de vos paramètres depuis le lien : https://ecobalyse.beta.gouv.fr/#/api')
        print("Utilisez la requête API : [GET]/textile/simulator - Calcul des impacts environnementaux d'un produit textile\n")
        print("Le type des paramètres peut évoluer selon les versions d'Ecobalyse : 'str' vers 'boolean', etc. Soyez attentif.")
        print("Le libellé des textiles peut évoluer selon les versions d'Ecobalyse : 'accents', 'parenthèses', etc. Soyez attentif.\n")
        print("Détails de l'échec : \n", result2.text)
        print('\n')
        return df_initial


def get_description_datas(df, params_dir, api_token, json_output_path):
    """
    Charge les paramètres de fichiers dans un répertoire, envoie des requêtes à l'API Ecobalyse pour obtenir des descriptions environnementales,
    met à jour un DataFrame avec ces informations et sauvegarde le DataFrame mis à jour en fichier JSON.

    Paramètres :
    -----------
    params_dir : str
        Le chemin du répertoire contenant les fichiers de paramètres.
    
    api_token : str
        Le jeton d'API utilisé pour l'autorisation de la requête API.
    
    json_output_path : str
        Le chemin du fichier JSON où le DataFrame mis à jour sera sauvegardé.

    Retour :
    --------
    pandas.DataFrame
        Le DataFrame mis à jour avec les descriptions obtenues de l'API pour les libellés correspondants.
    """
    # Charger les librairies utiles
    import os
    import pandas as pd
    import time
    
    start = time.time()
    
    print("Ajouter les descriptions des différents textiles ...")
    
    # Liste globale des paramètres
    params_list = []

    # Charger les paramètres de chaque fichier dans le répertoire 'data'
    for param_file in os.listdir(params_dir):
        if param_file.startswith('params') and param_file.endswith('.txt'):
            file_path = os.path.join(params_dir, param_file)
            params_list.extend(load_params_from_file(file_path))

    # Initialiser un DataFrame vide
    # df = pd.DataFrame()

    # Boucle pour traiter chaque ensemble de paramètres
    for params in params_list:
        data = create_textile_data(params)
        df = find_description(df, data, api_token)

    # Calculer le temps de traitement
    end = time.time()
    runtime = end - start
    
    # Afficher le DataFrame mis à jour
    if df is not None and not df.empty:
        print(f"DataFrame mis à jour avec succès au bout de : {runtime:.2f} secondes.")
        
        # Afficher toutes les colonnes
        pd.set_option('display.max_columns', None)    
        print(df.head(7))
        
        # Sauvegarder le DataFrame mis à jour en fichier JSON
        df.to_json(json_output_path, orient='records', lines=True)
        print("\nDataFrame sauvegardé en fichier json, avec succès.")
        
    else:
        print("Échec de la mise à jour du DataFrame, ou DataFrame vide.")

    return df