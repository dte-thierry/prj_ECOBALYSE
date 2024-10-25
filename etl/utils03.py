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


def calculate_pourcentage_etapes(df_initial, data):
    """
    Calcule les pourcentages d'impact environnemental de chaque étape du cycle de vie des textiles et met à jour un DataFrame avec ces informations.

    Cette fonction récupère les différents impacts environnementaux des matières premières, de la transformation, des compléments,
    de l'utilisation, de la fin de vie et du transport, puis calcule le pourcentage d'impact de chaque étape par rapport à l'écoscore total.
    Les résultats sont ajoutés au DataFrame initial.

    Paramètres :
    -----------
    df_initial : pandas.DataFrame
        Le DataFrame initial à mettre à jour avec les pourcentages d'impact environnemental de chaque étape.
    
    data : dict
        Les données contenant les informations de base des textiles.

    Retour :
    --------
    pandas.DataFrame
        Le DataFrame mis à jour avec les pourcentages d'impact environnemental de chaque étape.
    """
    # Charger les librairies utiles
    import math
    
    # Récupération des différents impacts environnementaux de chaque étape
    # ecs : impacts environnementaux globaux
    ecs_info = df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'ecs'].values[0]    
    # ecs_materials, ecs_transformation, ecs_complementsImpacts, ecs_utilisation, ecs_fin_de_vie
    ecs_materials_info = df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'ecs_materials'].values[0]
    ecs_transformation_info = df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'ecs_transformation'].values[0]
    ecs_complementsImpacts_info = df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'ecs_complementsImpacts'].values[0]
    ecs_utilisation_info = df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'ecs_utilisation'].values[0]
    ecs_fin_de_vie_info = df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'ecs_fin_de_vie'].values[0]
    # ecs_transport
    ecs_transport_info = df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'ecs_transport'].values[0]
    # coefficient de durabilité
    durability_info = df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'durability'].values[0]
    
    # Calcul de l'écoscore 'ecs' à partir des sous-impacts et des compléments 
    ecs_calcul = round((ecs_materials_info + ecs_transformation_info + ecs_complementsImpacts_info + ecs_utilisation_info + ecs_fin_de_vie_info) / durability_info, 2)
    # Arrondir le résultat à l'entier supérieur
    ecs_calcul = math.ceil(ecs_calcul)
    
    # Mise à jour de la colonne 'ecs' si les valeurs 'ecs' sont différentes
    if ecs_info != ecs_calcul:
        df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'ecs'] = ecs_calcul    
    
    # Pourcentages de l'impact environnemental de chaque étape (en %)
    matieres_premieres = round(((ecs_materials_info / durability_info) / ecs_calcul)*100, 2)
    transformation = round(((ecs_transformation_info / durability_info) / ecs_calcul)*100, 2)
    emballage = 0.0
    transports = round(((ecs_transport_info / durability_info) / ecs_calcul)*100, 2)
    distribution = 0.0
    utilisation = round(((ecs_utilisation_info / durability_info) / ecs_calcul)*100, 2)
    fin_de_vie = round(((ecs_fin_de_vie_info / durability_info) / ecs_calcul)*100, 2)
    
    # liste des différents pourcentages 
    infos_etapes = [{'matieres_premieres': matieres_premieres, 'transformation': transformation, 'emballage': emballage, 'transports': transports, 
                     'distribution': distribution, 'utilisation': utilisation, 'fin_de_vie': fin_de_vie}]
    
    # Ajout de la colonne 'Etapes'
    df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'Etapes'] = infos_etapes
    
    return df_initial


def get_impacts_finDeVie(df_initial, df_lifeCycle, data):
    """
    Met à jour un DataFrame avec les impacts environnementaux de la fin de vie des textiles.

    Cette fonction récupère les impacts environnementaux de la fin de vie à partir des données fournies,
    et met à jour le DataFrame initial avec cette information.

    Paramètres :
    -----------
    df_initial : pandas.DataFrame
        Le DataFrame initial à mettre à jour avec les impacts environnementaux de la fin de vie.
    
    df_lifeCycle : pandas.DataFrame
        Le DataFrame contenant les informations du cycle de vie des textiles.
    
    data : dict
        Les données contenant les informations de base des textiles.

    Retour :
    --------
    pandas.DataFrame
        Le DataFrame mis à jour avec les impacts environnementaux de la fin de vie.
    """
    
    # Récupérer les impacts : ecs_fin-de-vie
    fin_de_vie_info = df_lifeCycle[df_lifeCycle['label'] == 'Fin de vie']['impacts'].iloc[0] # récupérer la colonne 'impacts'
    ecs_fin_de_vie_info = fin_de_vie_info['ecs']
    ecs_fin_de_vie_info = round(ecs_fin_de_vie_info / 1.0, 2)
    # print('ecs_fin_de_vie : ' + str(ecs_fin_de_vie_info))
    
    # Ajout de la colonne ecs_fin_de_vie
    df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'ecs_fin_de_vie'] = ecs_fin_de_vie_info
    
    return df_initial


def get_impacts_utilisation(df_initial, df_lifeCycle, data):
    """
    Met à jour un DataFrame avec les impacts environnementaux de l'utilisation des textiles.

    Cette fonction récupère les impacts environnementaux de l'utilisation à partir des données fournies,
    et met à jour le DataFrame initial avec cette information.

    Paramètres :
    -----------
    df_initial : pandas.DataFrame
        Le DataFrame initial à mettre à jour avec les impacts environnementaux de l'utilisation.
    
    df_lifeCycle : pandas.DataFrame
        Le DataFrame contenant les informations du cycle de vie des textiles.
    
    data : dict
        Les données contenant les informations de base des textiles.

    Retour :
    --------
    pandas.DataFrame
        Le DataFrame mis à jour avec les impacts environnementaux de l'utilisation.
    """
    
    # Récupérer les impacts : ecs_utilisation
    utilisation_info = df_lifeCycle[df_lifeCycle['label'] == 'Utilisation']['impacts'].iloc[0] # récupérer la colonne 'impacts'
    ecs_utilisation_info = utilisation_info['ecs']
    ecs_utilisation_info = round(ecs_utilisation_info / 1.0, 2)
    # print('ecs_utilisation : ' + str(ecs_utilisation_info))
    
    # Ajout de la colonne ecs_utilisation
    df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'ecs_utilisation'] = ecs_utilisation_info
    
    return df_initial


def get_impacts_distribution(df_initial, df_lifeCycle, data):
    """
    Met à jour un DataFrame avec les impacts environnementaux de la distribution des textiles.

    Cette fonction récupère les impacts environnementaux de la distribution à partir des données fournies,
    et met à jour le DataFrame initial avec cette information.

    Paramètres :
    -----------
    df_initial : pandas.DataFrame
        Le DataFrame initial à mettre à jour avec les impacts environnementaux de la distribution.
    
    df_lifeCycle : pandas.DataFrame
        Le DataFrame contenant les informations du cycle de vie des textiles.
    
    data : dict
        Les données contenant les informations de base des textiles.

    Retour :
    --------
    pandas.DataFrame
        Le DataFrame mis à jour avec les impacts environnementaux de la distribution.
    """
    
    # - Total : impacts distribution
    distribution_info = df_lifeCycle[df_lifeCycle['label'] == 'Distribution']['impacts'].iloc[0] # récupérer la colonne 'impacts'
    ecs_distribution_info = distribution_info['ecs']
    ecs_distribution_info = round(ecs_distribution_info / 1.0, 2)
    # print('ecs_distribution : ' + str(ecs_distribution_info))

    # Ajout de la colonne ecs_distribution
    df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'ecs_distribution'] = ecs_distribution_info
    
    return df_initial


def get_impacts_transport(df_initial, df_transport, data):
    """
    Met à jour un DataFrame avec les impacts environnementaux du transport des textiles.

    Cette fonction récupère les impacts environnementaux du transport à partir des données fournies,
    et met à jour le DataFrame initial avec cette information.

    Paramètres :
    -----------
    df_initial : pandas.DataFrame
        Le DataFrame initial à mettre à jour avec les impacts environnementaux du transport.
    
    df_transport : pandas.DataFrame
        Le DataFrame contenant les valeurs des impacts environnementaux du transport.
    
    data : dict
        Les données contenant les informations de base des textiles.

    Retour :
    --------
    pandas.DataFrame
        Le DataFrame mis à jour avec les impacts environnementaux du transport.
    """
    
    # récupérer les impacts : Transport
    transport_list = df_transport[df_transport['Nom'] == 'impacts']['Valeur'].iloc[0] # récupérer la colonne 'Nom'

    # Afficher les impacts : ecs_transport
    ecs_transport_info = transport_list['ecs']
    ecs_transport_info = round(ecs_transport_info / 1.0, 2)
    # print('ecs_transport : ' + str(ecs_transport_info))

    # Ajout de la colonne ecs_transport
    df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'ecs_transport'] = ecs_transport_info
    
    return df_initial


def get_impacts_emballage(df_initial, data):
    """
    Met à jour un DataFrame avec les impacts environnementaux de l'emballage des textiles.

    Cette fonction calcule les impacts environnementaux de l'emballage (initialisé à zéro dans ce cas),
    et met à jour le DataFrame initial avec cette information.

    Paramètres :
    -----------
    df_initial : pandas.DataFrame
        Le DataFrame initial à mettre à jour avec les impacts environnementaux de l'emballage.
    
    data : dict
        Les données contenant les informations de base des textiles.

    Retour :
    --------
    pandas.DataFrame
        Le DataFrame mis à jour avec les impacts environnementaux de l'emballage.
    """
    
    total_emballage = 0
    ecs_emballage_info = round(total_emballage / 1.0, 2)
    # print('ecs_emballage : ' + str(ecs_emballage_info))

    # Ajout de la colonne ecs_emballage
    df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'ecs_emballage'] = ecs_emballage_info
    
    return df_initial


def get_complements_impacts(df_initial, df_complementsImpacts, data):
    """
    Met à jour un DataFrame avec les impacts environnementaux complémentaires des textiles.

    Cette fonction calcule le total des impacts environnementaux complémentaires à partir des données fournies,
    et met à jour le DataFrame initial avec cette information.

    Paramètres :
    -----------
    df_initial : pandas.DataFrame
        Le DataFrame initial à mettre à jour avec les impacts environnementaux complémentaires.
    
    df_complementsImpacts : pandas.DataFrame
        Le DataFrame contenant les valeurs des impacts environnementaux complémentaires.
    
    data : dict
        Les données contenant les informations de base des textiles.

    Retour :
    --------
    pandas.DataFrame
        Le DataFrame mis à jour avec les impacts environnementaux complémentaires.
    """
    
    # - Total des impacts complémentaires
    total_complementsImpacts = df_complementsImpacts['Valeur'].sum()
    ecs_complementsImpacts_info = round(total_complementsImpacts / 1.0, 2)
    # print('ecs_complementsImpacts : ' + str(ecs_complementsImpacts_info))
    
    # Ajout de la colonne ecs_complementsImpacts
    df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'ecs_complementsImpacts'] = ecs_complementsImpacts_info
    
    return df_initial


def get_impacts_materials_transformation(df_initial, df_lifeCycle, data):
    """
    Met à jour un DataFrame avec les impacts environnementaux des matières premières et des étapes de transformation des textiles.

    Cette fonction récupère les impacts environnementaux des matières premières et des différentes étapes de transformation
    (filature, tissage, ennoblissement, confection) à partir des données du cycle de vie, et met à jour le DataFrame initial
    avec ces informations.

    Paramètres :
    -----------
    df_initial : pandas.DataFrame
        Le DataFrame initial à mettre à jour avec les impacts environnementaux.
    
    df_lifeCycle : pandas.DataFrame
        Le DataFrame contenant les informations du cycle de vie des textiles.
    
    data : dict
        Les données contenant les informations de base des textiles.

    Retour :
    --------
    pandas.DataFrame
        Le DataFrame mis à jour avec les impacts environnementaux des matières premières et des étapes de transformation.
    """
    
    # Récupérer l'impact : ecs_materials
    impacts_info = df_lifeCycle[df_lifeCycle['label'] == 'Matières premières']['impacts'].iloc[0] # récupérer la colonne 'impacts'
    ecs_materials_info = impacts_info['ecs']
    ecs_materials_info = round(ecs_materials_info / 1.0, 2)     
    # Ajout de la colonne ecs_materials
    df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'ecs_materials'] = ecs_materials_info
    
    # Récupérer les impacts : ecs_filature, ecs_tissage, ecs_ennoblissement, et ecs_confection 
    # - ecs_filature
    impacts_info = df_lifeCycle[df_lifeCycle['label'] == 'Filature']['impacts'].iloc[0] # récupérer la colonne 'impacts'
    ecs_filature_info = impacts_info['ecs']
    # - ecs_tissage
    impacts_info = df_lifeCycle[df_lifeCycle['label'] == 'Tissage & Tricotage']['impacts'].iloc[0] # récupérer la colonne 'impacts'
    ecs_tissage_info = impacts_info['ecs']
    # - ecs_ennoblissement
    impacts_info = df_lifeCycle[df_lifeCycle['label'] == 'Ennoblissement']['impacts'].iloc[0] # récupérer la colonne 'impacts'
    ecs_ennoblissement_info = impacts_info['ecs']
    # - ecs_confection
    impacts_info = df_lifeCycle[df_lifeCycle['label'] == 'Confection']['impacts'].iloc[0] # récupérer la colonne 'impacts'
    ecs_confection_info = impacts_info['ecs']
    
    # - Total des impacts de l'étape : Transformation
    ecs_transformation_info = round((ecs_filature_info + ecs_tissage_info + ecs_ennoblissement_info + ecs_confection_info) / 1.0, 2)
    # print('ecs_transformation : ' + str(ecs_transformation_info))
    
    # Ajout de la colonne ecs_transformation
    df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'ecs_transformation'] = ecs_transformation_info
    
    return df_initial


def get_basics_inputs(df_initial, data, df_inputs):
    """
    Met à jour un DataFrame avec les informations de base des textiles à partir des données fournies et des paramètres d'entrée.

    Cette fonction ajoute des colonnes au DataFrame initial avec des informations telles que le business, le nombre de références,
    le prix, la traçabilité, le produit, le ratio de transport aérien, les matières premières, et les pays de filature, de fabrication,
    de teinture et de confection.

    Paramètres :
    -----------
    df_initial : pandas.DataFrame
        Le DataFrame initial à mettre à jour avec les informations de base des textiles.
    
    data : dict
        Les données contenant les informations de base des textiles.
    
    df_inputs : pandas.DataFrame
        Le DataFrame contenant les paramètres d'entrée extraits de l'API.

    Retour :
    --------
    pandas.DataFrame
        Le DataFrame mis à jour avec les informations de base des textiles.
    """
    
    # Ajouter les colonnes : 'business', 'numberOfReferences', 'price', 'traceability', 'product', 'airtransportRatio'     
    df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'business'] = data['business']
    df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'numberOfReferences'] = data['numberOfReferences']
    df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'price'] = data['price']
    df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'traceability'] = data['traceability']
    df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'product'] = data['product']
    df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'airTransportRatio'] = data['airTransportRatio']
    
    # récupérer la liste des matières premières
    materials_list = df_inputs[df_inputs['Nom'] == 'materials']['Valeur'].iloc[0] # récupérer la colonne 'Nom'
    
    # extraire les informations minimales uniquement
    materials_info = [{'id': item['material']['id'], 'share': item['share']} for item in materials_list]

    # Si materials_info est une liste, convertir chaque élément en chaîne de caractères
    if isinstance(materials_info, list):
        materials_info = ', '.join([str(item) if isinstance(item, dict) else item for item in materials_info])    
    # Ajouter la colonne : 'materials'
    df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'materials'] = materials_info  
    
    # Ajouter les colonnes : 'countrySpinning', 'countryFabric', 'countryDyeing', 'countryMaking' 
    df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'countrySpinning'] = data['countrySpinning']
    df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'countryFabric'] = data['countryFabric']
    df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'countryDyeing'] = data['countryDyeing']
    df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'countryMaking'] = data['countryMaking']
    
    return df_initial


def find_details(df_initial, data, api_token):
    """
    Envoie des requêtes à l'API Ecobalyse pour obtenir des descriptions environnementales détaillées,
    met à jour un DataFrame avec ces informations et retourne le DataFrame mis à jour.

    Paramètres :
    -----------
    df_initial : pandas.DataFrame
        Le DataFrame initial à mettre à jour avec les détails des textiles.
    
    data : dict
        Les données à envoyer à l'API pour obtenir les détails des textiles.
    
    api_token : str
        Le jeton d'API utilisé pour l'autorisation de la requête API.

    Retour :
    --------
    pandas.DataFrame
        Le DataFrame mis à jour avec les descriptions obtenues de l'API pour les libellés correspondants.
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
    result2 = requests.post(link + 'textile/simulator/detailed', headers=headers, json=data) # passage des paramètres 'data'
    
    # Vérifiez le statut de la requête
    if result2.status_code == 200:
        # Convertir la réponse en JSON
        response_json = result2.json()
        
        # Extraire la liste des paramètres dans un DataFrame
        df_inputs = pd.DataFrame(response_json['inputs'].items(), columns=['Nom', 'Valeur'])
        
        # Extraire les informations du cycle de vie dans un DataFrame
        df_lifeCycle = pd.DataFrame(response_json['lifeCycle'])
        
        # Extraire la liste des impacts environnementaux dans un DataFrame
        df_impacts = pd.DataFrame(response_json['impacts'].items(), columns=['Nom', 'Impacts Environnementaux (Pts)'])
        
        # Extraire la liste des compléments d'impacts dans un DataFrame
        df_complementsImpacts = pd.DataFrame(response_json['complementsImpacts'].items(), columns=['Nom', 'Valeur'])
        
        # Extraire les informations de transport dans un DataFrame 
        df_transport = pd.DataFrame(response_json['transport'].items(), columns=['Nom', 'Valeur']) 
        
        # Trouver l'index de la ligne où 'Nom' est 'ecs'
        index = df_impacts[df_impacts['Nom'] == 'ecs'].index[0]

        # Extraire la valeur 'ecs'
        ecs_value = df_impacts.loc[index, 'Impacts Environnementaux (Pts)']
        
        # Arrondir à l'entier supérieur
        # ecs_value = math.ceil(ecs_value)

        # Convertir à l'entier inférieur
        ecs_value = math.floor(ecs_value)
        
        # Remplacer la valeur 'ecs' dans les DataFrames (df_impacts, df_initial) par la valeur arrondie (ou convertie)
        df_impacts.loc[index, 'Impacts Environnementaux (Pts)'] = ecs_value        
        df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'ecs'] = ecs_value
        
        # Ajouter les paramètres d'entrée : 'business', 'numberOfReferences', 'price', 'traceability', 'product', 'airTransportRatio', 'materials',
        #                                   'countrySpinning', 'countryFabric', 'countryDyeing', 'countryMaking'
        df_initial = get_basics_inputs(df_initial, data, df_inputs) 
        
        # Ajouter le Coefficient de durabilité : 'durability'
        durability_info = response_json['durability']
        df_initial.loc[df_initial['Libelle'].str.contains(data['libelle']), 'durability'] = durability_info
        
        # Récupérer les impacts : 'ecs_materials', 'ecs_transformation'
        df_initial = get_impacts_materials_transformation(df_initial, df_lifeCycle, data)
        
        # Récupérer les compléments d'impacts environnementaux (microfibers, outOfEuropeEOL, etc.)- : 'ecs_complementsImpacts'
        df_initial = get_complements_impacts(df_initial, df_complementsImpacts, data)
        
        # Récupérer l'impact : 'ecs_emballage'
        # df_initial = get_impacts_emballage(df_initial, data)
        
        # Récupérer l'impact : 'ecs_transport'
        df_initial = get_impacts_transport(df_initial, df_transport, data)
        
        # Récupérer l'impact : 'ecs_distribution'
        # df_initial = get_impacts_distribution(df_initial, df_lifeCycle, data)
        
        # Récupérer l'impact : 'ecs_utilisation'
        df_initial = get_impacts_utilisation(df_initial, df_lifeCycle, data)
        
        # Récupérer l'impact : 'ecs_finDeVie'
        df_initial = get_impacts_finDeVie(df_initial, df_lifeCycle, data)
        
        # Calculer le pourcentage d'impact de chaque étape : 'Etapes'
        df_initial = calculate_pourcentage_etapes(df_initial, data)
        
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



def get_details_datas(df, params_dir, api_token, json_output_path):
    """
    Charge les paramètres de fichiers dans un répertoire, envoie des requêtes à l'API pour obtenir des descriptions environnementales détaillées,
    met à jour un DataFrame avec ces informations et sauvegarde le DataFrame mis à jour en fichier JSON.

    Paramètres :
    -----------
    df : pandas.DataFrame
        Le DataFrame à mettre à jour avec les détails des textiles.
    
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
    
    print("\nCalculer les impacts détaillés des différents textiles ...")
    
    # Liste globale des paramètres
    params_list = []

    # Charger les paramètres de chaque fichier dans le répertoire 'data'
    for param_file in os.listdir(params_dir):
        if param_file.startswith('params') and param_file.endswith('.txt'):
            file_path = os.path.join(params_dir, param_file)
            params_list.extend(load_params_from_file(file_path))

    # Boucle pour traiter chaque ensemble de paramètres
    for params in params_list:
        data = create_textile_data(params)
        df = find_details(df, data, api_token)

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

