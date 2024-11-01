from pymongo import MongoClient
import json
from jsonschema import validate, ValidationError

import os

# Connexion à MongoDB
client = MongoClient('mongodb://admin:admin@localhost:27017/')

# Supprimer la base de données 'ecobalyse' si elle existe
client.drop_database('ecobalyse')

# Créer (recréer) la base de données 'ecobalyse'
db = client['ecobalyse']

# Vérifier si la collection 'textiles' existe avant de la créer
if 'textiles' not in db.list_collection_names():
    db.create_collection('textiles')

# Définir le schéma JSON
schema = {
    "type": "object",
    "properties": {
        "Libelle": {"type": "string"},
        "Categorie": {"type": "string"},
        "ecs": {"type": "number"},
        "Pays": {"type": "string"},
        "Mode": {"type": "string"},
        "Masse": {"type": "number"},
        "Matiere": {"type": "string"},
        "description": {"type": "string"},
        "business": {"type": "string"},
        "numberOfReferences": {"type": "number"},
        "price": {"type": "number"},
        "traceability": {"type": "boolean"},
        "product": {"type": "string"},
        "airTransportRatio": {"type": "number"},
        "materials": {"type": "string"},
        "countrySpinning": {"type": "string"},
        "countryFabric": {"type": "string"},
        "countryDyeing": {"type": "string"},
        "countryMaking": {"type": "string"},
        "durability": {"type": "number"},
        "ecs_materials": {"type": "number"},
        "ecs_transformation": {"type": "number"},
        "ecs_complementsImpacts": {"type": "number"},
        "ecs_transport": {"type": "number"},
        "ecs_utilisation": {"type": "number"},
        "ecs_fin_de_vie": {"type": "number"},
        "Etapes": {
            "type": "object",
            "properties": {
                "matieres_premieres": {"type": "number"},
                "transformation": {"type": "number"},
                "emballage": {"type": "number"},
                "transports": {"type": "number"},
                "distribution": {"type": "number"},
                "utilisation": {"type": "number"},
                "fin_de_vie": {"type": "number"}
            },
            "required": ["matieres_premieres", "transformation", "emballage", "transports", "distribution", "utilisation", "fin_de_vie"]
        }
    },
    "required": ["Libelle", "Categorie", "ecs", "Pays", "Mode", "Masse", "Matiere", "Etapes"]
}

# Vérifier que les variables d'environnement sont définies
if not all([os.getenv('JSON_BASIC_FILE'), os.getenv('JSON_FULL_FILE'), os.getenv('PROG_FULL_MODE')]):
    raise EnvironmentError("Les variables d'environnement JSON_BASIC_FILE, JSON_FULL_FILE, et PROG_FULL_MODE doivent être définies.")

# Récupérer les variables d'environnement
PROG_FULL_MODE = os.getenv('PROG_FULL_MODE') == 'True'
JSON_BASIC_FILE = os.getenv('JSON_BASIC_FILE')
JSON_FULL_FILE = os.getenv('JSON_FULL_FILE')

# Définir le chemin du fichier JSON en fonction du mode
if PROG_FULL_MODE:
    json_file_path = os.path.join('/app/data', JSON_FULL_FILE)
else:
    json_file_path = os.path.join('/app/data', JSON_BASIC_FILE)

# Lire les données du fichier JSON ligne par ligne
# json_file_path = '/app/data/PRJ-ECOBALYSE-01-WEB_SCRAPING1_temp1.json'
with open(json_file_path, 'r') as file:
    for line in file:
        line = line.strip()  # Supprimer les espaces blancs en début et fin de ligne
        if line:  # Vérifier que la ligne n'est pas vide
            try:
                document = json.loads(line)
            except json.JSONDecodeError:
                print(f"Erreur de décodage JSON pour la ligne : {line}")
                continue
            
            # Ajouter des valeurs par défaut pour les champs manquants sans écraser les valeurs existantes
            defaults = {
                "description": "",
                "business": "",
                "numberOfReferences": 0,
                "price": 0.0,
                "traceability": False,
                "product": "",
                "airTransportRatio": 0.0,
                "materials": "",
                "countrySpinning": "",
                "countryFabric": "",
                "countryDyeing": "",
                "countryMaking": "",
                "durability": 0.0,
                "ecs_materials": 0.0,
                "ecs_transformation": 0.0,
                "ecs_complementsImpacts": 0.0,
                "ecs_transport": 0.0,
                "ecs_utilisation": 0.0,
                "ecs_fin_de_vie": 0.0,
                "Etapes": {
                    "matieres_premieres": 0.0,
                    "transformation": 0.0,
                    "emballage": 0.0,
                    "transports": 0.0,
                    "distribution": 0.0,
                    "utilisation": 0.0,
                    "fin_de_vie": 0.0
                }
            }
            
            for key, value in defaults.items():
                if key not in document:
                    document[key] = value
                elif isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        if sub_key not in document[key]:
                            document[key][sub_key] = sub_value
            
            try:
                validate(instance=document, schema=schema)
                
                # Convertir le champ Etapes en dictionnaire Python si nécessaire
                if isinstance(document["Etapes"], str):
                    document["Etapes"] = json.loads(document["Etapes"].replace("'", '"'))
                
                db.textiles.insert_one(document)
            except ValidationError as e:
                print(f"Validation error for document: {document}")
                print(e)

# Afficher les documents de la collection 'textiles'
print("\nDocuments ajoutés dans la collection 'textiles' :")
for doc in db.textiles.find():
    print(doc)

# Afficher toutes les catégories de textiles
print("\nCatégories de textiles :")
categories = db.textiles.distinct('Categorie')
for category in categories:
    print(category)

# Afficher toutes les modes disponibles
print("\nModes disponibles :")
modes = db.textiles.distinct('Mode')
for mode in modes:
    print(mode)

# Afficher toutes les catégories de textiles avec le libellé et le score ecs minimal
print("\nCatégories de textiles avec le score ECS minimal :")
pipeline_min = [
    {
        "$group": {
            "_id": "$Categorie",
            "libelle": {"$first": "$Libelle"},
            "min_ecs": {"$min": "$ecs"}
        }
    }
]

results_min = db.textiles.aggregate(pipeline_min)
for result in results_min:
    print(f"Categorie: {result['_id']}, Libelle: {result['libelle']}, ecs minimal: {result['min_ecs']}")

# Afficher toutes les catégories de textiles avec le libellé et le score ecs maximal
print("\nCatégories de textiles avec le score ECS maximal :")
pipeline_max = [
    {
        "$group": {
            "_id": "$Categorie",
            "libelle": {"$first": "$Libelle"},
            "max_ecs": {"$max": "$ecs"}
        }
    }
]

results_max = db.textiles.aggregate(pipeline_max)
for result in results_max:
    print(f"Categorie: {result['_id']}, Libelle: {result['libelle']}, ecs maximal: {result['max_ecs']}")

