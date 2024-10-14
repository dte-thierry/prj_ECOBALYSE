import requests
import pandas as pd
import numpy as np
import random
import os
from requests.exceptions import RequestException

# Fonctions auxiliaires
def get_random_mass(min=0.1, max=0.3, pas=0.03):
    return np.random.choice(np.arange(min, max, pas))

def get_random_country():
    country_values = ['BD', 'KH', 'CN', 'FR', '---', 'IN', 'MA', 'MM', 'PK', 'RAF', 'RLA', 
                      'RNA', 'RAS', 'REE', 'REO', 'RME', 'ROC', 'TN', 'TR', 'VN']
    return np.random.choice(country_values)

def get_random_airTransportRatio():
    airTransportRatio_values = [0, 0.33, 1]
    return np.random.choice(airTransportRatio_values)

def get_random_price_tshirt():
    initial_price = 10    
    max_percentage = (40 - initial_price) / initial_price    
    random_percentage = np.random.uniform(0, max_percentage)    
    final_price = initial_price * (1 + random_percentage)
    return int(np.ceil(final_price))

def get_random_traceability():
    return random.choice([True, False])

def get_random_business():
    return np.random.choice(['small-business', 'large-business-with-services', 'large-business-without-services'])

def get_random_fabricProcess():
    return np.random.choice(['knitting-mix', 'knitting-fully-fashioned', 'knitting-integral',
                             'knitting-circular', 'knitting-straight', 'weaving'])

def get_random_marketingDuration(seasonal_variability=120, quarterly_variability=240, prolonged_period=360):
    durations = [seasonal_variability, quarterly_variability, prolonged_period]
    chosen_duration = random.choice(durations)
    marketing_duration = random.randint(1, chosen_duration)
    return min(marketing_duration, 999)

def get_random_numberOfReferences(min_value=150, max_value=150000, step=200):
    num_steps = (max_value - min_value) // step
    random_steps = random.randint(0, num_steps)
    return min_value + random_steps * step

def get_random_materials(material_ids):
    assert len(material_ids) == 3, "La liste des identifiants de matériaux doit contenir exactement trois éléments."
    first_share = round(random.uniform(0.5, 1.0), 2)
    second_share = round(random.uniform(0.0, 1.0 - first_share), 2)
    third_share = round(1.0 - first_share - second_share, 2)
    return [
        {'id': material_ids[0], 'share': first_share},
        {'id': material_ids[1], 'share': second_share},
        {'id': material_ids[2], 'share': third_share}
    ]

def choose_random_materials_tshirt():
    materials_lists = [
        ['ei-coton', 'ei-pet', 'ei-lin'],
        ['ei-coton', 'ei-pet', 'ei-viscose'],
        ['ei-coton', 'ei-lin', 'ei-viscose'],
        ['ei-pet', 'ei-lin', 'ei-viscose'],
        ['ei-coton', 'ei-chanvre', 'ei-viscose'],
        ['ei-pet', 'ei-chanvre', 'ei-viscose'],
        ['ei-lin', 'ei-chanvre', 'ei-viscose']
    ]
    return random.choice(materials_lists)

def get_random_data_tshirt():
    mass = get_random_mass()
    material_ids = choose_random_materials_tshirt()
    materials = get_random_materials(material_ids)
    product = 'tshirt'
    countrySpinning = get_random_country()
    countryFabric = get_random_country()
    countryDyeing = countryFabric
    countryMaking = countryFabric
    airTransportRatio = get_random_airTransportRatio()
    fabricProcess = get_random_fabricProcess()
    business = get_random_business()
    marketingDuration = get_random_marketingDuration()
    numberOfReferences = get_random_numberOfReferences()
    price = get_random_price_tshirt()
    traceability = get_random_traceability()
    
    nomTshirt = f'Tshirt ({int(mass*1000)}g) - C: {countryMaking} - ATR: {int(airTransportRatio*100)}% - {price}€.'
    
    random_data = {
        'mass': mass,
        'materials': materials,
        'product': product,
        'countrySpinning': countrySpinning,
        'countryFabric': countryFabric,
        'countryDyeing': countryDyeing,
        'countryMaking': countryMaking,
        'airTransportRatio': airTransportRatio,
        'fabricProcess': fabricProcess,
        'business': business,
        'marketingDuration': marketingDuration,
        'numberOfReferences': numberOfReferences,
        'price': price,
        'traceability': traceability
    }
    
    return random_data, nomTshirt, mass, countrySpinning, countryFabric, countryDyeing, countryMaking, fabricProcess, \
           business, marketingDuration, numberOfReferences, traceability

def create_random_tshirts(n=10):
    link = 'https://ecobalyse.beta.gouv.fr/api/'
    df_total = pd.DataFrame()

    for i in range(n):
        try: 
            data, nomTshirt, mass, countrySpinning, countryFabric, countryDyeing, countryMaking, fabricProcess, \
                             business, marketingDuration, numberOfReferences, traceability = get_random_data_tshirt()

            result2 = requests.post(link + 'textile/simulator', json=data)

            if result2.status_code == 200:
                response_json = result2.json()
                df_impacts = pd.DataFrame(response_json['impacts'].items(), columns=['nom', f'{i+1} - {nomTshirt}'])
                df_transpose = df_impacts.transpose()
                df_transpose.columns = df_transpose.iloc[0]
                df_transpose = df_transpose[1:]
                df_transpose['ecs'] = np.ceil(df_transpose['ecs'])
                df_transpose['pef'] = np.ceil(df_transpose['pef'])
                df_transpose['description'] = response_json['description']
                df_total = pd.concat([df_total, df_transpose])
            else:
                print('La requête a échoué avec le code de statut :', result2.status_code)

        except Exception as e:
            print("Une erreur s'est produite :", e)

    output_dir = '/data'
    os.makedirs(output_dir, exist_ok=True)
    
    df_total.to_json(f'{output_dir}/api_random{n}_t-shirt_data_out.json', orient='split', force_ascii=False)
    df_total.to_csv(f'{output_dir}/api_random{n}_t-shirt_data_out.csv', encoding='utf-8', index=True)
    
    return df_total

if __name__ == "__main__":
    n_tshirts = int(os.environ.get('N_TSHIRTS', 100))
    
    print(f"Génération de {n_tshirts} t-shirts aléatoires...")
    df_results = create_random_tshirts(n_tshirts)
    print("Génération terminée. Les résultats ont été sauvegardés dans le répertoire /data.")
    
    
    
    '''
    Commandes pour lancer docker et l'exécuter 
    Pour utiliser ce Dockerfile :

Assurez-vous d'avoir les fichiers suivants dans le même répertoire :

Dockerfile (avec le contenu ci-dessus)
requirements.txt (avec les dépendances requises)
ecobalyse_generator.py (votre script Python complet)


Construisez l'image Docker :
Copydocker build -t ecobalyse-generator .

Exécutez le conteneur :
Copydocker run -v /chemin/vers/dossier/local:/data -e N_TSHIRTS=1000 ecobalyse-generator


Cette configuration vous permettra d'exécuter votre script Python dans un environnement Docker isolé, tout en sauvegardant les résultats dans un dossier sur votre machine hôte.
'''
    
    
    