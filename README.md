<img src="img/PRJ-ECOBALYSE-00-LOGO.png" alt="Logo DataScientest" style="width:250px;height:auto;">

# Datascientest: [projet EcoBalyse](./PRJ-ECOBALYSE-00-FICHE_PROJET.pdf) (Nov. 2024)

## Sommaire
- [Contexte](#tdm-01)
- [Présentation](#tdm-02)
- [Mode d'emploi](#tdm-03)
- [Etapes du projet](#tdm-04)
- [Solution technique](#tdm-05)
- [A propos d'Ecobalyse](#tdm-06)

## <a name="tdm-01" />Contexte :
Ce projet a été réalisé dans le cadre de la formation continue de Data Engineer, proposée par :  
<a href="https://datascientest.com/formation-data-engineer" target="_blank">Datascientest et l'Ecole des Mines ParisTech</a>.

L'équipe ayant réalisé ce projet se compose de :
* SERDYUK Alexandra
* BENALLEGUE Anis
* DELIGNE Thierry

## <a name="tdm-02" />Présentation
Basé sur les données, et l'`API` de calcul des impacts environnementaux d'[Ecobalyse v2.4.0](https://ecobalyse.beta.gouv.fr/), ce projet permet : 
- d'obtenir une évaluation de l'impact écologique de textiles courants
- potentiellement, de fournir des recommandations ou des conseils sur des alternatives plus durables

<br />
<img src="img/PRJ-ECOBALYSE-00-IMG2.jpg" alt="Présentation" style="width:750px;height:auto;">

## <a name="tdm-03" />Mode d'emploi

### Pré-requis

- installer [VS Code](https://code.visualstudio.com/) localement sur votre PC, en fonction de votre système d'exploitation.

- configurer `VS Code` pour pouvoir accéder, via <i>SSH</i>, à la machine virtuelle DataSientest.

- lancer et accéder à la machine virtuelle DataScientest, depuis le lien : <br />
*https://learn.datascientest.com/lesson/349/3682*

- recopier le dépôt GitHub sur la machine virtuelle, par la commande : <br />
*git clone https://github.com/dte-thierry/prj_ECOBALYSE.git*

- au besoin, lancer le script `info.sh` pour vérifier que Docker est bien installé, par la commande : <br />
*./info.sh*

<br />
Puis, depuis le répertoire <i><b>~/prj_ECOBALYSE</i></b> :

- au besoin, lancer le script `stop.sh` pour arrêter les services, par la commande : <br />
*./stop.sh*

- au besoin, lancer le script `reset.sh` pour supprimer tous les conteneurs, images, volumes, et réseaux inutilisés, par la commande : <br />
*./reset.sh*

#### Facultatif :

- (au besoin, lancer le script `start.sh` pour exécuter l'extraction des données Ecobalyse, par la commande : <br />
*./start.sh*)

- (via VS Code, consulter le contenu du fichier .log  `'manual_webscraping_(date).log' ` pour vérifier l'extraction des données Ecobalyse. <br />


### Lancement

#### Lancer les services
- lancer le script `setup.sh` pour activer les différents conteneurs et services nécessaires au projet, par la commande : <br />
*./setup.sh*

## <a name="tdm-04" />Etapes du projet
- Etape 01 : [récolte des données](notebooks/PRJ-ECOBALYSE-01-WEB_SCRAPING1_v0-20.ipynb)
- Etape 02 : architecture de la donnée
- Etape 03 : consommation de la donnée
- Etape 04 : mise en production
- Etape 05 : automatisation des flux

## <a name="tdm-05" />Solution technique

### Schéma de principe

<img src="img/PRJ-ECOBALYSE-00-IMG3.png" alt="Schéma de principe" style="width:750px;height:auto;">

La solution proposée se compose de : 

* Un `ETL` qui a la charge de récupérer les contenus d'Ecobalyse.

* Une base de données `MongoDB` où sont entreprosées les données récupérées.

* Un dashboard `Dash`.

* Une API `FastApi` permettant au dashboard de requêter la base de données.

* Un DAG `Airflow` pour gérer l'orchestration de l'ETL

### Arborescence des dossiers et fichiers

prj_ECOBALYSE
<br />├── data
<br />│   ├── mongo
<br />│   └── redis
<br />│   ├── params01_T-shirt.txt
<br />│   ├── params02_Pull.txt
<br />│   ├── params03_Pantalon.txt
<br />│   ├── params04_Manteau.txt
<br />│   ├── params05_Maillot-de-bain.txt
<br />│   ├── params06_Jupe.txt
<br />│   ├── params07_Jean.txt
<br />│   ├── params08_Chemise.txt
<br />│   ├── params09_Chaussettes.txt
<br />│   ├── params10_Calecon.txt
<br />│   ├── params11_Slip.txt
<br />│   └── PRJ-ECOBALYSE-01-WEB_SCRAPING1_temp1.json
<br />├── etl
<br />│   ├── Dockerfile.etl
<br />│   ├── extract1.py
<br />│   ├── requirements.txt
<br />│   ├── utils01.py
<br />│   ├── utils02.py
<br />│   └── utils03.py
<br />├── img
<br />│   ├── PRJ-ECOBALYSE-00-IMG1.jpg
<br />│   ├── PRJ-ECOBALYSE-00-IMG2.jpg
<br />│   ├── PRJ-ECOBALYSE-00-IMG3.png
<br />│   └── PRJ-ECOBALYSE-00-LOGO.png
<br />├── logs
<br />│   ├── docker_testmongo_2024-10-27_18-26-08.log
<br />│   ├── docker_testredis_2024-10-27_18-26-07.log
<br />│   └── docker_webscraping_2024-10-27_18-26-00.log
<br />├── mongo
<br />│   ├── Dockerfile.mongo
<br />│   ├── init_mongo.js
<br />│   ├── init_mongo.sh
<br />│   ├── mongo.conf
<br />│   └── test_mongo.py
<br />├── notebooks
<br />│   ├── PRJ-ECOBALYSE-00-LOGO.png
<br />│   ├── PRJ-ECOBALYSE-01-WEB_SCRAPING1_v0-20.ipynb
<br />├── redis
<br />│   ├── Dockerfile.redis
<br />│   ├── init_redis.sh
<br />│   ├── redis.conf
<br />│   └── test_redis.py
<br />├── clear.sh
<br />├── CONVENTIONS.md
<br />├── docker-compose.yml
<br />├── info.sh
<br />├── LICENSE
<br />├── PRJ-ECOBALYSE-00-FICHE_PROJET.pdf
<br />├── README.md
<br />├── rebuild.sh
<br />├── reset.sh
<br />├── setup.sh
<br />├── start.sh
<br />└── stop.sh

## <a name="tdm-06" />A propos d'Ecobalyse
__Écobalyse__ est un outil développé par l'État français pour calculer l'impact écologique des produits textiles et alimentaires distribués en France. Il vise à fournir des informations sur l'empreinte environnementale de ces produits, permettant ainsi aux consommateurs de prendre des décisions plus éclairées  et durables sur leurs choix de consommation. 
    
En lien avec les préoccupations actuelles (l'industrie textile est l'une des plus polluantes au monde), __Écobalyse__ vise à accélérer la mise en place de l'affichage environnemental, pour favoriser un modèle de production plus durable.
    
__Voici quelques points clés à propos d'Écobalyse__ :
    
- `Objectif` : __Écobalyse__ permet de comprendre et de calculer les impacts écologiques des produits distribués en France.

- `Éco-score` : __Écobalyse__ propose un éco-score pour informer les consommateurs sur l'impact environnemental des produits qu'ils achètent.    
    
- `Collaboration ouverte` : __Écobalyse__ est un mode de collaboration ouvert à la critique et aux suggestions, dans le but d'aider à élaborer la future méthode réglementaire française.

- [`API ouverte`](https://api.gouv.fr/les-api/api-ecobalyse) : __Écobalyse__ propose une __interface de programmation applicative__ (__API__) pour connecter le calculateur Écobalyse à d'autres services numériques. L'[__API__](https://api.gouv.fr/les-api/api-ecobalyse) est testée dans le cadre de l'expérimentation Xtex, conformément à la loi Climat et Résilience.
    
    Ci-après quelques exemples d'utilisation de l'[__API__](https://api.gouv.fr/les-api/api-ecobalyse) __Écobalyse__ pour estimer les impacts environnementaux des produits textiles : 
    
        1. Interroger la base de données des indicateurs d'impacts environnementaux des produits textiles. 
        Récupérer des informations sur les impacts environnementaux d'un vêtement en fonction de critères tels que 
        la traçabilité, la matière et le recyclage.
    
        2. Calculer les impacts pour chaque produit.
        Estimer, pour chaque produit textile : l'impact carbone, l'impact sur la couche d'ozone, l'impact sur la 
        qualité de l'eau, le coût énergétique, l'impact sur l'eutrophisation de l'eau et des terres, l'impact sur 
        l'acidification terrestre des eaux douces, l'utilisation du sol, l'utilisation de minéraux. 

        3. Tester le simulateur.
        Explorer les impacts environnementaux de différents produits textiles.
    
Toutes marques, producteurs, ou distributeurs peutvent contribuer à améliorer le calcul d'impacts écologiques, en partageant leurs données et en participant aux travaux collectifs.
    
Pour en savoir plus, on peut visiter le site d'__Écobalyse__ [ici](https://ecobalyse.beta.gouv.fr/). 

__A voir également :__

- [GitBook `Écobalyse`](https://fabrique-numerique.gitbook.io/ecobalyse)
- [Explorateur `Écobalyse`](https://ecobalyse.beta.gouv.fr/#/explore/textile/processes)    
- [Documentation de `API` Écobalyse](https://api.gouv.fr/documentation/api-ecobalyse)
- [Ademe](https://affichage-environnemental.ademe.fr/)

<img src="img/PRJ-ECOBALYSE-00-IMG1.jpg" alt="A propos" style="width:750px;height:auto;">
