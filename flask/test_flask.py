import logging
from flask import Flask, render_template, flash, request, jsonify, url_for
from pymongo import MongoClient
from bson import ObjectId
import json
import time
import pandas as pd
import redis
import os

from datetime import datetime
from utils import impact_metrics, get_data_from_mongodb, get_data_from_redis, create_bar

# Configurer le logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Récupérer la variable d'environnement
flask_log_namefile = os.getenv('FLASK_LOG_NAMEFILE', 'default_log_name')

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

# Configuration du logging
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    log_filename = f"logs/{flask_log_namefile}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Application Flask active.")

# page d'accueil Flask
@app.route('/')
def home():    
    app.logger.info('Page d\'accueil affichée')
    return render_template('bienvenue.html')

# test : retourne la liste des BDD disponibles    
@app.route('/testflask')
def list_mongo_bdd():
    mongo_dbs = mongo_client.list_databases()
    flash("")
    dbs_info = [{'name': db['name'], 'sizeOnDisk': db['sizeOnDisk'] / (1024 * 1024)} for db in mongo_dbs]
    app.logger.info('Liste des bases MongoDB récupérée')
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
    app.logger.info('Données MongoDB récupérées')
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
        app.logger.info('Données Redis récupérées')
        return app.response_class(
            response=json.dumps(response, ensure_ascii=False),
            mimetype='application/json'
        )
    else:
        response = {
            "message": "Aucune donnée trouvée dans Redis.",
            "error": "No data found"
        }
        app.logger.warning('Aucune donnée trouvée dans Redis')
        return app.response_class(
            response=json.dumps(response, ensure_ascii=False),
            mimetype='application/json'
        ), 404


@app.route("/impact_metrics", methods=["GET", "POST"])
def display_impact_metrics():
    if request.method == "POST":
        # Gérer le formulaire POST si nécessaire
        pass
    
    # Récupérer les données de MongoDB et mesurer le temps de chargement
    df_mongodb, mongodb_time = get_data_from_mongodb()
    if df_mongodb is None:
        flash("Erreur: ensemble de données vide pour MongoDB.")
        return render_template("undone.html")
    
    # Récupérer les données de Redis et mesurer le temps de chargement
    df_redis, redis_time = get_data_from_redis()
    if df_redis is None:
        flash("Erreur: ensemble de données vide pour Redis.")
        return render_template("undone.html")
    
    # Flasher les temps de chargement
    flash(f"Temps de chargement des données via MongoDB : {mongodb_time:.2f} milliseconds")
    flash(f"Temps de chargement des données via Redis : {redis_time:.2f} milliseconds")
    
    metrics = impact_metrics()
    
    # Générer les données des graphiques en barres
    bar_chart_data_category = create_bar(
        list(metrics['avg_ecs_per_category'].keys()),
        list(metrics['avg_ecs_per_category'].values()),
        "EcoScore Moyen par Catégorie"
    )
    bar_chart_data_mode = create_bar(
        list(metrics['avg_ecs_per_mode'].keys()),
        list(metrics['avg_ecs_per_mode'].values()),
        "EcoScore Moyen par Mode"
    )
    bar_chart_data_country = create_bar(
        list(metrics['avg_ecs_per_country'].keys()),
        list(metrics['avg_ecs_per_country'].values()),
        "EcoScore Moyen par Pays"
    )
    
    # Vérification des données JSON avec logging
    logging.debug("bar_chart_data_category: %s", bar_chart_data_category)
    logging.debug("bar_chart_data_mode: %s", bar_chart_data_mode)
    logging.debug("bar_chart_data_country: %s", bar_chart_data_country)
    
    return render_template(
        "impact_metrics.html",
        metrics=metrics,
        bar_chart_data_category=bar_chart_data_category,
        bar_chart_data_mode=bar_chart_data_mode,
        bar_chart_data_country=bar_chart_data_country
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0')