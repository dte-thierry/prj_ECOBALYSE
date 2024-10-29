from flask import Flask, render_template, flash, request, jsonify, url_for
from pymongo import MongoClient
from bson import ObjectId
import json

import time
import redis

app = Flask(__name__, template_folder="templates", static_folder="stylesheets")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour utiliser flash

# Configuration MongoDB
mongo_client = MongoClient('mongodb://ecblmongodb:27017/')
mongo_db = mongo_client['ecobalyse']

# Configuration Redis
redis_client = redis.StrictRedis(host='ecblredis', port=6379, decode_responses=True)

# Custom JSON encoder for ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(JSONEncoder, self).default(obj)

# page d'accueil Flask
@app.route('/')
def home():    
    return render_template('bienvenue.html')


# test : retourne la liste des BDD disponibles    
@app.route('/testflask')
def list_mongo_bdd():
    mongo_dbs = mongo_client.list_databases()
    flash("")
    dbs_info = [{'name': db['name'], 'sizeOnDisk': db['sizeOnDisk'] / (1024 * 1024)} for db in mongo_dbs]
    return render_template('listMongoBDD.html', mongo_dbs=dbs_info)


# test : retourne un textile Ecobalyse enregistré dans MongoDB
@app.route('/testmongo')
def get_mongo_data():
    data = mongo_db.textiles.find_one()
    flash("Données Ecobalyse MongoDB récupérées avec succès !")
    response = {
        "message": "Exemple MongoDB de textile Ecobalyse : ",
        "data": json.loads(JSONEncoder().encode(data))
    }
    return app.response_class(
        response=json.dumps(response, ensure_ascii=False),
        mimetype='application/json'
    )


# test : retourne un textile Ecobalyse enregistré dans Redis
@app.route('/testredis')
def get_redis_data():
    keys = redis_client.keys('textile:*')
    if keys:
        first_key = keys[0]
        data = redis_client.hgetall(first_key)
        flash("Données Ecobalyse Redis récupérées avec succès !")
        response = {
            "message": "Exemple Redis de textile Ecobalyse : ",
            "data": json.loads(JSONEncoder().encode(data))
        }
        return app.response_class(
            response=json.dumps(response, ensure_ascii=False),
            mimetype='application/json'
        )
    else:
        response = {
            "message": "Aucune donnée trouvée dans Redis.",
            "error": "No data found"
        }
        return app.response_class(
            response=json.dumps(response, ensure_ascii=False),
            mimetype='application/json'
        ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0')