# utils.py
import logging
import pandas as pd
import redis
import math
import time

import json
import plotly
import plotly.graph_objs as go

from pymongo import MongoClient

# Configurer le logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_data_from_redis():
    try:
        start_time = time.time()
        logger.info("Connexion à Redis...")
        r = redis.Redis(host='ecblredis', port=6379, decode_responses=True, health_check_interval=30)
        logger.info("Connexion établie.")
        
        keys = r.keys('textile:*')
        logger.info(f"Nombre de clés récupérées : {len(keys)}")
        
        if not keys:
            logger.warning("Aucune clé trouvée dans Redis.")
            return None
        
        data = []
        for key in keys:
            textile_info = r.hgetall(key)
            data.append(textile_info)
        
        df = pd.DataFrame(data)
        if 'ecs' in df.columns:
            df['ecs'] = pd.to_numeric(df['ecs'], errors='coerce')
        
        df.columns = df.columns.str.strip()  # Supprimer les espaces autour des noms de colonnes
        logger.info(f"Colonnes du DataFrame : {df.columns}")  # Vérifier les colonnes
        logger.info(f"Premières lignes du DataFrame :\n{df.head()}")  # Afficher les premières lignes du DataFrame
        
        end_time = time.time()
        execution_time_ms = (end_time - start_time) * 1000
        logger.info(f"Temps de chargement des données via Redis : {execution_time_ms:.2f} milliseconds")
        
        return df, execution_time_ms
    
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des données de Redis : {e}")
        return None, None

def get_data_from_mongodb():
    try:
        start_time = time.time()
        logger.info("Connexion à MongoDB...")
        mongo_client = MongoClient('mongodb://ecblmongodb:27017/')
        mongo_db = mongo_client['ecobalyse']
        logger.info("Connexion établie.")
        
        collection = mongo_db['textiles']
        data = list(collection.find())
        logger.info(f"Nombre de documents récupérés : {len(data)}")
        
        if not data:
            logger.warning("Aucune donnée trouvée dans la collection 'textile'.")
            return None, None
        
        df = pd.DataFrame(data)
        if 'ecs' in df.columns:
            df['ecs'] = pd.to_numeric(df['ecs'], errors='coerce')
        df.columns = df.columns.str.strip()  # Supprimer les espaces autour des noms de colonnes
        logger.info(f"Colonnes du DataFrame : {df.columns}")  # Vérifier les colonnes
        logger.info(f"Premières lignes du DataFrame :\n{df.head()}")  # Afficher les premières lignes du DataFrame
        
        end_time = time.time()
        execution_time_ms = (end_time - start_time) * 1000
        logger.info(f"Temps de chargement des données via MongoDB : {execution_time_ms:.2f} milliseconds")
        
        return df, execution_time_ms
    
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des données de MongoDB : {e}")
        return None, None

def impact_metrics():
    df, _ = get_data_from_mongodb()  # Ignorer le temps de chargement ici
    if df is None or df.empty:
        return None
    metrics = {
        'avg_ecs_per_category': {k: math.ceil(v) for k, v in df.groupby('Categorie')['ecs'].mean().to_dict().items()},
        'avg_ecs_per_mode': {k: math.ceil(v) for k, v in df.groupby('Mode')['ecs'].mean().to_dict().items()},
        'avg_ecs_per_country': {k: math.ceil(v) for k, v in df.groupby('Pays')['ecs'].mean().to_dict().items()}
    }
    return metrics


def impact1_metrics():
    df, _ = get_data_from_mongodb()  # Ignorer le temps de chargement ici
    if df is None or df.empty:
        return None
    
    # Calculer les statistiques de distribution pour les scores environnementaux
    distribution_stats = {
        'min_ecs': df['ecs'].min(),
        'max_ecs': df['ecs'].max(),
        '25th_percentile': df['ecs'].quantile(0.25),
        'median_ecs': df['ecs'].median(),
        '75th_percentile': df['ecs'].quantile(0.75),
        'mean_ecs': df['ecs'].mean(),
        'std_dev_ecs': df['ecs'].std()
    }
    
    # Identifier les produits avec des scores particulièrement élevés ou bas
    high_ecs_products = df[df['ecs'] >= distribution_stats['75th_percentile']]
    low_ecs_products = df[df['ecs'] <= distribution_stats['25th_percentile']]
    
    metrics = {
        'distribution_stats': distribution_stats,
        'high_ecs_products': high_ecs_products.to_dict(orient='records'),
        'low_ecs_products': low_ecs_products.to_dict(orient='records')
    }
    
    return metrics


def create_bar(x_data, y_data, title):
    import logging
    logging.debug("Creating bar chart with x_data: %s and y_data: %s", x_data, y_data)
    
    data = [
        {
            "x": x_data,
            "y": y_data,
            "type": "bar"
        }
    ]
    layout = {
        "title": {"text": title},
        "template": {
            "data": {
                "histogram2dcontour": [{"type": "histogram2dcontour", "colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}],
                "choropleth": [{"type": "choropleth", "colorbar": {"outlinewidth": 0, "ticks": ""}}],
                "histogram2d": [{"type": "histogram2d", "colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}],
                "heatmap": [{"type": "heatmap", "colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}],
                "heatmapgl": [{"type": "heatmapgl", "colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}]
            }
        }
    }
    return {"data": data, "layout": layout}