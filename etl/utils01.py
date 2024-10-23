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
