import redis
import json

if __name__ == "__main__":
    r = redis.Redis(host='ecblredis', port=6379, decode_responses=True, health_check_interval=30)
    print("Redis fonctionne et le fichier JSON est bien récupéré : ", r.ping())

    # Supprimer l'ensemble 'textiles' s'il existe
    r.delete('textiles')

    # Lire le fichier JSON ligne par ligne et convertir en tableau JSON
    with open('/app/data/PRJ-ECOBALYSE-01-WEB_SCRAPING1_temp1.json', 'r') as input_file:
        lines = input_file.readlines()
        libelles = [json.loads(line) for line in lines]
    
    # Ajouter les données à Redis
    for info in libelles:
        libelle = info['Libelle']
        # Convertir toutes les valeurs en chaînes de caractères
        info_str = {k: str(v) for k, v in info.items()}
        r.hset(f'textile:{libelle}', mapping=info_str)

    # Récupérer et afficher les données de Redis
    keys = r.keys('textile:*')
    categories_min = {}
    categories_max = {}
    for key in keys:
        textile_info = r.hgetall(key)
        categorie = textile_info.get('Categorie', 'Unknown')
        ecs = float(textile_info.get('ecs', float('inf')))
        
        # Convertir les étapes en dictionnaire Python
        etapes_str = textile_info.get('Etapes', '{}').replace("'", '"')
        try:
            etapes = json.loads(etapes_str)
        except json.JSONDecodeError:
            etapes = {}

        if categorie not in categories_min or ecs < categories_min[categorie]['ecs']:
            categories_min[categorie] = {
                'Libelle': textile_info['Libelle'],
                'ecs': ecs,
                'Etapes': etapes
            }
        
        if categorie not in categories_max or ecs > categories_max[categorie]['ecs']:
            categories_max[categorie] = {
                'Libelle': textile_info['Libelle'],
                'ecs': ecs,
                'Etapes': etapes
            }
        
        print(f"Libelle: {textile_info['Libelle']}, ecs: {textile_info['ecs']}, autres colonnes: {textile_info}")

    # Afficher toutes les catégories de textiles avec le libellé, le score ecs minimal, 
    # et l'impact intermédiaire des différentes étapes
    print("\nCatégories de textiles avec le score ECS minimal :")
    for categorie, info in categories_min.items():
        print(f"Categorie: {categorie}, Libelle: {info['Libelle']}, ecs minimal: {info['ecs']}")
        print("Etapes montrant les impacts intermédiaires (en pourcentage) :")
        for etape, impact in info['Etapes'].items():
            print(f"  {etape}: {impact} %")

    # Afficher toutes les catégories de textiles avec le libellé, le score ecs maximal, 
    # et l'impact intermédiaire des différentes étapes
    print("\nCatégories de textiles avec le score ECS maximal :")
    for categorie, info in categories_max.items():
        print(f"Categorie: {categorie}, Libelle: {info['Libelle']}, ecs maximal: {info['ecs']}")
        print("Etapes montrant les impacts intermédiaires (en pourcentage) :")
        for etape, impact in info['Etapes'].items():
            print(f"  {etape}: {impact} %")