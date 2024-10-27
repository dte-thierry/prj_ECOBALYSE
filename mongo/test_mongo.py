from pymongo import MongoClient
import json

# Connexion à MongoDB
client = MongoClient('mongodb://admin:admin@localhost:27017/')

# Supprimer la base de données 'ecobalyse' si elle existe
client.drop_database('ecobalyse')

# Afficher les bases de données existantes
print("Bases de données existantes :")
print(client.list_database_names())

# Créer (recréer) la base de données 'ecobalyse'
db = client['ecobalyse']

# Afficher un message indiquant la base de données utilisée
print(f"Base de données nouvellement créée : {db.name}")

# Vérifier si la collection 'textiles' existe avant de la créer
if 'textiles' not in db.list_collection_names():
    db.create_collection('textiles')

# Lire les données du fichier JSON ligne par ligne
json_file_path = '/app/data/PRJ-ECOBALYSE-01-WEB_SCRAPING1_temp1.json'
with open(json_file_path, 'r') as file:
    for line in file:
        document = json.loads(line)
        db.textiles.insert_one(document)

# Afficher les documents de la collection 'textiles'
print("Documents ajoutés dans la collection 'textiles' :")
for doc in db.textiles.find():
    print(doc)