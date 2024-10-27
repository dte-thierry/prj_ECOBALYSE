import redis
import json

if __name__ == "__main__":
    r = redis.Redis(host='redis', port=6379, decode_responses=True, health_check_interval=30)
    print("Redis fonctionne et le fichier JSON est bien récupéré : ", r.ping())

    # Supprimer l'ensemble 'textiles' s'il existe
    r.delete('textiles')

    # Lire le fichier JSON ligne par ligne et convertir en tableau JSON
    with open('/app/data/PRJ-ECOBALYSE-01-WEB_SCRAPING1_temp1.json') as input_file:
        lines = input_file.readlines()
        libelles = [json.loads(line) for line in lines]
    
    # Ajouter les données à Redis
    for info in libelles:
        libelle = info['Libelle']
        ecs = info['ecs']
        r.zadd('textiles', {libelle: ecs})

    # Récupérer et afficher les données de Redis par un set ordonné
    textiles = r.zrange('textiles', 0, -1, withscores=True)
    for libelle, ecs in textiles:
        print(f"Libelle: {libelle}, ecs: {ecs}")
            