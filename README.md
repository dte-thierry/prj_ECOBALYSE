<a name="debut" />

<img src="img/PRJ-ECOBALYSE-00-LOGO.png" alt="Logo DataScientest" style="width:250px;height:auto;">

# Datascientest: [projet EcoBalyse](./PRJ-ECOBALYSE-00-FICHE_PROJET.pdf) (Nov. 2024)
> *Data Engineering End-to-End Project : AirFlow, Dash, Flask, Docker, Redis, MongoDB, Python* <br />

Dernière Mise A Jour du Document : Mer. 06/11/2024 - Version : v0.2.0

## [Sommaire](#debut)
- [Contexte](#tdm-01)
- [Présentation](#tdm-02)
    - [Etapes du projet](#tdm-02-01)
- [Mode d'emploi](#tdm-03)
    - [Pré-requis (`./info.sh` | `./mode.sh` | `./starter.sh`)](#tdm-03-01)
    - [(Ré)Initialiser (`./init.sh`)](#tdm-03-02)
    - [(Re)Configurer (`./setup.sh`)](#tdm-03-03)
    - [(Re)Charger (`./load.sh`)](#tdm-03-04)
- [Solution technique](#tdm-05)
    - [Schéma de Principe](#tdm-05-01)
    - [Dossiers & Répertoires](#tdm-05-02)
- [Détails techniques](#tdm-07)
    - [Architecture](#tdm-07-07)
    - [ETL](#tdm-07-01)
    - [MongoDB](#tdm-07-02)
    - [Redis](#tdm-07-03)
    - [Flask](#tdm-07-04)
    - [Dash](#tdm-07-05)
    - [AirFlow](#tdm-07-06)
- [A propos d'Ecobalyse](#tdm-06)

## <a name="tdm-01" />[Contexte](#debut)
Ce projet a été réalisé dans le cadre de la <b>formation Data Engineer</b>, proposée par :  
<a href="https://datascientest.com/formation-data-engineer" target="_blank">Datascientest, et l'Ecole des Mines ParisTech</a>.

Le *[cursus pédagogique](./img/DATASCIENTEST_ParcoursPedagogique.png)* de la <b>formation Data Engineer</b> s'inscrit dans le cadre de la **[certification n°RNCP36129](https://www.francecompetences.fr/recherche/rncp/36129/)** :  
*“Chef de projet en intelligence artificielle / (Machine Learning Engineer)”, Niveau 7 (bac + 5)*.  

L'équipe ayant réalisé ce projet se compose de :
* SERDYUK Alexandra
* BENALLEGUE Anis
* DELIGNE Thierry

Le **Rapport Final**, expliquant tout le workflow décisionnel du projet, est disponible : [ici](./ecblRapport.pdf).

## <a name="tdm-02" />[Présentation](#debut)
Basé sur les données, et l'`API` de calcul des impacts environnementaux d'[Ecobalyse v2.4.0](https://ecobalyse.beta.gouv.fr/), ce projet doit permettre : 
- d'obtenir une évaluation de l'impact écologique de textiles courants
- de fournir des recommandations ou des conseils sur des alternatives plus durables

<br />
<img src="img/PRJ-ECOBALYSE-00-IMG2.jpg" alt="Présentation" style="width:750px;height:auto;">

### <a name="tdm-02-01" />[Etapes du projet](#tdm-02)

> 💬 **Nota : Par défaut, la récolte des données se fait en mode `Basic`.** <br />
> Lancer le script `./mode.sh -f` pour définir une récolte des données en mode `Complet`.

- **Etape 01 : récolte des données** <br />
[Extraction](notebooks/PRJ-ECOBALYSE-01-ETAPE-01-BASIC_v0-20.ipynb) (mode `Basic`), [Transformation](notebooks/PRJ-ECOBALYSE-02-ETAPE-01-FULL_v0-20.ipynb) (mode `Complet`)

    - Identification de la source de données
    - Connexion et importation des données

- **Etape 02 : architecture & stockage**

    - Choix d'un SGBD adapté au problème
    - Modélisation des tables/collections/index

- **Etape 03 : consommation des données** <br />
`Visualisations` (mode: [Basic](notebooks/PRJ-ECOBALYSE-03-ETAPE-03-VISU-BASIC_v0-20.ipynb) | [Complet](notebooks/PRJ-ECOBALYSE-04-ETAPE-03-VISU-FULL_v0-20.ipynb)) , `Prédictions` (mode: [Basic](notebooks/PRJ-ECOBALYSE-05-ETAPE-03-ML-BASIC_v0-20.ipynb) | [Complet](notebooks/PRJ-ECOBALYSE-06-ETAPE-03-ML-FULL_v0-20.ipynb))

    - Dashboard ou Algorithme de Machine Learning (périmètre du *Data Scientist/Analyst*)

- **Etape 04 : mise en production**

    - Création de l'API du projet
    - Dockerisation de tout le projet

- **Etape 05 : automatisation des flux (<i>Etape facultative</i>)**

    - Automatisation des tâches avec AirFlow

## <a name="tdm-03" />[Mode d'emploi](#debut)

### <a name="tdm-03-01" />[Pré-requis (`./info.sh` | `./mode.sh` | `./starter.sh`)](#tdm-03)

| 💬 Avertissement ! Le client Docker doit être installé sur la machine virtuelle. |
|----------|
| Pour (ré)installer, ou mettre à jour le client **Docker**, consulter le fichier [lisezMoi.txt](./lisezMoi.txt). | 

> 💬 **Nota : action préalable facultative à l'extraction des données Ecobalyse** <br />
> Une fois le dépôt GitHub recopié, vous pouvez spécifier le **mode d'extraction des données** *(Basic | Complet)* depuis le script :
> `./mode.sh`.

> **Résumé du(des) script(s) utile(s)**
>
> - `./info.sh -v` # affiche la version du client Docker installé (nota: ./info.sh <b>-?</b> renvoie les options disponibles)
> - `./info.sh -i` # affiche la liste des images Docker présentes 
> - `./info.sh -a` # affiche la liste des conteneurs Docker actifs
> - `./info.sh -df` # affiche l'espace disque disponible
>
> **Résumé du(des) script(s) facultatif(s)**
>
> - `./mode.sh -f` # configure le mode d'extraction **(Complet)** des données Ecobalyse. Fixe le nombre de données aléatoires, par catégories de textiles.
> - `./mode.sh` # configure le mode d'extraction **(Basic)** des données Ecobalyse. 
> - `./starter.sh -i` # vérifie l'extraction des Données Ecobalyse (nota: ./starter.sh <b>-?</b> renvoie les options disponibles)
> - `./starter.sh` # idem : vérifie l'extraction des Données Ecobalyse

#### Configurer VS Code

- installer [VS Code](https://code.visualstudio.com/) localement sur votre PC, en fonction de votre système d'exploitation.

- configurer [VS Code](https://code.visualstudio.com/) pour pouvoir accéder, via <i>SSH</i>, à la machine virtuelle DataSientest.

#### Lancer la machine virtuelle

- accéder, puis lancer la machine virtuelle DataScientest, depuis le lien : <br /> `https://learn.datascientest.com/lesson/349/3682`

#### Recopier le dépôt Github

- recopier le dépôt GitHub sur la machine virtuelle, par la commande : <br /> `git clone https://github.com/dte-thierry/prj_ECOBALYSE.git`

#### Vérifier la version  

- au besoin, depuis le répertoire <i><b>~/prj_ECOBALYSE</i></b>, une fois le dépôt GitHub recopié, lancer le script : <br />
`./info.sh -v`, pour vérifier la version du client Docker installé. (nota: `./info.sh -?` renvoie les options disponibles)

#### 💬 Facultatif 

- Le mode d'extraction des données (Basic | Complet) **peut être choisi au préalable** de l'extraction <i>"standard" des données</i> Ecobalyse. Lancer le script `./mode.sh`, pour préciser votre choix. (nota: `./mode.sh -?` renvoie les options disponibles)

- puis, depuis le répertoire <i><b>~/prj_ECOBALYSE</i></b>, lancer le script `./starter.sh -i` pour tester l'extraction <i>"standard"</i> (hors conteneur **Docker**) des données Ecobalyse.
  
- via [VS Code](https://code.visualstudio.com/), depuis le répertoire */logs*, consulter le contenu du fichier `'manual_webscraping_(date).log'`, pour vérifier le résultat obtenu.

##### 💬 Nota 

Vous pouvez lancer le script `./starter.sh`, <b>sans aucune option</b>. 

En lançant le script `./starter.sh -i`, en fonction du **mode d'extraction des données** (Basic | Complet), vous obtiendrez les messages d'avertissement suivants :

###### Mode Basic

```bash
--------------------------------------------------------------
ETAPE 01 : Récupération des Données via l'API Ecobalyse v2.4.0
--------------------------------------------------------------
VM utilisée, à l'adresse IP / SSH publique : 54.154.13.241

Mode d'Extraction Des Données : Basic. 
Fichier JSON à créer : PRJ-ECOBALYSE-TEXTILES_basic.json

Avertissement:
--------------
L'API d'Ecobalyse est actuellement non finalisée, toujours en cours de développement.
Ce projet se base sur l'API d'Ecobalyse : v2.4.0 pour récupérer les données.
Soyez attentif et vigilant à la récupération des données Ecobalyse obtenues, via l'API.
Consultez dans le répertoire /logs, le fichier .log : (manual|docker)_webscraping_(aaaa-mm-jj_hh-mn).log.
Vérifiez qu'aucune description de textile (colonne 'description') ne soit de type : NaN


DataFrame, fichiers 'log' et 'json' PRJ-ECOBALYSE-TEXTILES_basic.json créés avec succès, en mode basic.
```

###### Mode Complet

```bash
--------------------------------------------------------------
ETAPE 01 : Récupération des Données via l'API Ecobalyse v2.4.0
--------------------------------------------------------------
VM utilisée, à l'adresse IP / SSH publique : 54.154.13.241

Mode d'Extraction Des Données : Complet, avec ajout et transformation de données aléatoires. 
Fichier JSON à créer : PRJ-ECOBALYSE-TEXTILES_full.json

Avertissement:
--------------
L'API d'Ecobalyse est actuellement non finalisée, toujours en cours de développement.
Ce projet se base sur l'API d'Ecobalyse : v2.4.0 pour récupérer les données.
Soyez attentif et vigilant à la récupération des données Ecobalyse obtenues, via l'API.
Consultez dans le répertoire /logs, le fichier .log : (manual|docker)_webscraping_(aaaa-mm-jj_hh-mn).log.
Vérifiez qu'aucune description de textile (colonne 'description') ne soit de type : NaN


DataFrame, fichiers 'log' et 'json' PRJ-ECOBALYSE-TEXTILES_full.json créés avec succès, en mode complet.
```

### <a name="tdm-03-02" />[(Ré)Initialiser (`./init.sh`)](#tdm-03)

> **Résumé du(des) script(s) utile(s)**
>
> - `./init.sh` # supprime toutes les données (si elles existent) et (ré)initialise totalement la configuration du projet

#### Supprimer les conteneurs

Depuis le répertoire <i><b>~/prj_ECOBALYSE</i></b> :

- lancer le script `./init.sh` pour supprimer toutes les données (*logs* et *json*), et tous les conteneurs, images, volumes, réseaux inutilisés.

### <a name="tdm-03-03" />[(Re)Configurer (`./setup.sh`)](#tdm-03)

> **Résumé du(des) script(s) utile(s)**
>
> - `./setup.sh` # supprime les fichiers *.log*, et (re)lance les différents conteneurs du projet 
> - `./info.sh -logs` # visualise les logs des conteneurs actifs : *ecblwebscraping* , *ecblmongodb* , *ecblredis* 
>
> **Résumé du(des) script(s) facultatif(s)**
>
> - `./setup.sh -json` # supprime les fichiers *.log*, **les fichiers *.json*,** et (re)lance les différents conteneurs du projet 

#### Lancer les services

- lancer le script `./setup.sh` pour supprimer les fichiers *.log*, et (re)lancer les différents conteneurs du projet.

#### Visualiser les logs des conteneurs actifs

- puis, lancer le script `./info.sh -logs` pour visualiser les logs des conteneurs (re)lancés : *ecblwebscraping* , *ecblmongodb* , *ecblredis*.

#### Consulter les fichiers .log

- via [VS Code](https://code.visualstudio.com/), consulter le contenu des fichiers .log, pour vérifier que l'environnement de stockage `MongoDB` / `Redis` est fonctionnel. 
    - `'docker_webscraping_(date).log'` : pour visualiser l'extraction des données Ecobalyse, par les services
    - `'docker_testmongodb_(date).log'` : pour visualiser l'accès à MongoDB (et requêtes initiales) par les services
    - `'docker_testredis_(date).log'` : pour visualiser l'accès à Redis (et requêtes initiales) par les services

#### 💬 Facultatif 

- au besoin, lancer le script `./setup.sh -json` pour supprimer les fichiers *.log*, **les fichiers *.json*,** et (re)lancer les différents conteneurs du projet


### <a name="tdm-03-04" />[(Re)Charger (`./load.sh`)](#tdm-03)

> **Résumé du(des) script(s) utile(s)**
>
> - `./load.sh` # accède via un *navigateur Web* au Framework **Dash** 
> - `./load.sh -adm` # accède via un *navigateur Web* au Framework **Flask** 

#### Lancer Dash

- lancer le script `./load.sh` pour lancer `Dash` via un *navigateur Web*. <br />

- via [VS Code](https://code.visualstudio.com/), consulter le contenu du fichier .log, pour vérifier que l'application `Dash` est active. <br />
    - `'docker_testdash_(date).log'` 

<br />

La page d'accueil `Dash` s'affiche avec les informations suivantes :

...

##### 💬 Nota 

Lorsque le Framework Web `Dash` est démarré, via le conteneur *ecbldash*, on peut y accéder depuis un navigateur Web : <br />

- soit par l'adresse locale : 127.0.0.1:8050/
- soit par l'adresse IP / SSH publique de la VM, par exemple : 3.252.141.140:8050/

#### Lancer Flask

- lancer le script `./load.sh -adm` pour lancer `Flask` via un *navigateur Web*. <br />

- via [VS Code](https://code.visualstudio.com/), consulter le contenu du fichier .log, pour vérifier que l'application `Dash` est active. <br />
    - `'docker_testflask_(date).log'` 

<br />

La page d'accueil `Flask` s'affiche avec les informations suivantes :

```html
Accueil
Bienvenue sur la page d'accueil de votre application Flask !

Pour vérifier le bon fonctionnement de votre application, saisir les adresses :

127.0.0.1:5000/testflask, afin de lister les BDD MongoDB
127.0.0.1:5000/testmongo, afin de vérifier le contenu Ecobalyse de la BDD MongoDB
127.0.0.1:5000/testredis, afin de vérifier le contenu Ecobalyse de la BDD Redis
```

##### 💬 Nota 

Lorsque le Framework Web `Flask` est démarré, via le conteneur *ecblflask*, on peut y accéder depuis un navigateur Web : <br />

- soit par l'adresse locale : 127.0.0.1:5050/
- soit par l'adresse IP / SSH publique de la VM, par exemple : 3.252.141.140:5050/

## <a name="tdm-05" />[Solution technique](#debut)

### <a name="tdm-05-01" />[Schéma de principe](#tdm-05)

<img src="img/PRJ-ECOBALYSE-00-IMG3.png" alt="Schéma de principe" style="width:750px;height:auto;">

La solution proposée se compose de : 

* Un `ETL` qui a la charge de récupérer les contenus d'Ecobalyse.

* Une base de données `MongoDB` où sont entreprosées les données récupérées.
  
* Une base de données `Redis` utilisée comme mémoire cache, afin d'accélérer les requêtes.

* Un dashboard `Dash`.

* Un Framework Web `Flask` qui sert d’intermédiaire (API) entre le dashboard `Dash`, les bases de données `MongoDB` / `Redis`, et un modèle `scikit-learn` entraîné pour des prédictions de <b>Machine Learning</b>.

* Un DAG `Airflow` pour gérer l'orchestration de l'ETL.

### <a name="tdm-05-02" />[Dossiers & Répertoires](#tdm-05)

```bash
prj_ECOBALYSE
├── data
│   ├── mongo
│   ├── redis
│   ├── params01_T-shirt.txt
│   ├── params02_Pull.txt
│   ├── params03_Pantalon.txt
│   ├── params04_Manteau.txt
│   ├── params05_Maillot-de-bain.txt
│   ├── params06_Jupe.txt
│   ├── params07_Jean.txt
│   ├── params08_Chemise.txt
│   ├── params09_Chaussettes.txt
│   ├── params10_Calecon.txt
│   └── params11_Slip.txt
├── dag
├── dash
├── etl
├── flask
├── img
├── logs
├── mongo
├── notebooks
├── redis
├── PRJ-ECOBALYSE-00-FICHE_PROJET.pdf
├── LICENSE
├── CONVENTIONS.md
├── README.md
├── docker-compose.yml
├── lisezMoi.txt
├── info.sh
├── load.sh
├── setup.sh
├── init.sh
└── starter.sh
```

## <a name="tdm-07" />[Détails techniques](#debut)

### <a name="tdm-07-07" />[Architecture](#tdm-07)

#### docker-compose.yml
```bash
version: '3.8'

services:
  ecblwebscraping:
    build:
      context: . # contexte de construction à la racine du projet
      dockerfile: etl/Dockerfile.etl # chemin relatif vers le Dockerfile
    environment:
      - SERVICE_NAME=ecblwebscraping # variable d’environnement pour le service
    container_name: ecblwebscraping
    volumes:
      - ./logs:/app/logs # répertoire logs de l’hôte dans le conteneur
      - ./data:/app/data # répertoire data de l’hôte dans le conteneur
    networks:
      - my_ecobalyse_network # réseau dédié pour le service

  ecblredis:
    build:
      context: . # contexte de construction à la racine du projet
      dockerfile: redis/Dockerfile.redis # chemin relatif vers le Dockerfile pour Redis
    environment:
      - SERVICE_NAME=ecblredis # variable d’environnement pour le service
    container_name: ecblredis
    ports:
      - "6379:6379"
    volumes:
      - ./logs:/app/logs # répertoire logs de l’hôte dans le conteneur
      - ./data:/app/data # répertoire data de l’hôte dans le conteneur
    networks:
      - my_ecobalyse_network

  ecblmongodb:
    build:
      context: . # contexte de construction à la racine du projet
      dockerfile: mongo/Dockerfile.mongo # chemin relatif vers le Dockerfile pour MongoDB
    environment:
      - SERVICE_NAME=ecblmongodb # variable d’environnement pour le service
    container_name: ecblmongodb
    ports:
      - "27017:27017"
    volumes:
      - ./data/mongo:/data/db # répertoire data/mongo de l’hôte dans le conteneur
      - ./logs:/app/logs # répertoire logs de l’hôte dans le conteneur
      - ./data:/app/data # répertoire data de l’hôte dans le conteneur
    networks:
      - my_ecobalyse_network
  
  ecblflask:
    build:
      context: . # contexte de construction à la racine du projet
      dockerfile: flask/Dockerfile.flask # chemin relatif vers le Dockerfile pour Flask
    environment:
      - SERVICE_NAME=ecblflask # variable d’environnement pour le service
      - MONGO_URI=mongodb://ecblmongodb:27017
      - REDIS_URI=redis://ecblredis:6379
    container_name: ecblflask
    ports:
      - "5000:5000"
    depends_on:
      - ecblmongodb
      - ecblredis
    volumes:
      - ./logs:/app/logs # répertoire logs de l’hôte dans le conteneur
    networks:
      - my_ecobalyse_network

networks:
  my_ecobalyse_network:
    name: my_ecobalyse_network

volumes:
  logs:
  data:
```

### <a name="tdm-07-01" />[ETL](#tdm-07)

#### Dossiers & Répertoires

```bash
.
├── etl
│   ├── Dockerfile.etl
│   ├── constants.py
│   ├── extract1.py
│   ├── get_constants.py
│   ├── requirements.txt
│   ├── utils01.py
│   ├── utils02.py
│   └── utils03.py
.
```

#### Logs du conteneur

conteneur : ecblwebscraping
```bash
Affichage des logs du conteneur : ecblwebscraping...
Attaching to ecblwebscraping
ecblwebscraping    | --------------------------------------------------------------
ecblwebscraping    | ETAPE 01 : Récupération des Données via l'API Ecobalyse v2.4.0
ecblwebscraping    | --------------------------------------------------------------
ecblwebscraping    | VM utilisée, à l'adresse IP / SSH publique : 18.201.106.14
ecblwebscraping    | DataFrame, fichiers 'log' et 'json' créés avec succès, par le conteneur.
ecblwebscraping    | 
ecblwebscraping    |
```

#### Dockerfile

fichier : Dockerfile.etl
```bash
# Utiliser l'image Selenium avec Chrome
FROM selenium/standalone-chrome:latest

# Installer Python, pip, Xvfb et les dépendances nécessaires
USER root
RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y python3.8 python3.8-venv python3.8-dev build-essential xvfb

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires dans l'image Docker
COPY etl/ /app/
COPY starter.sh /app/

# Créer un environnement virtuel Python avec Python 3.8
RUN python3.8 -m venv venv

# Activer l'environnement virtuel et installer les dépendances Python
RUN /bin/bash -c "source venv/bin/activate && pip install --no-cache-dir -r /app/requirements.txt"

# Déclarer les volumes pour les répertoires logs et data
VOLUME ["/app/logs", "/app/data"]

# Définir la commande par défaut pour exécuter le script
CMD ["bash", "starter.sh"]
```

### <a name="tdm-07-02" />[MongoDB](#tdm-07)

#### Dossiers & Répertoires

```bash
.
├── mongo
│   ├── Dockerfile.mongo
│   ├── constants1.py
│   ├── get_constants1.py
│   ├── init_mongo.js
│   ├── init_mongo.sh
│   ├── mongo.conf
│   └── test_mongo.py
.
```

#### Logs du conteneur

conteneur : ecblmongodb
```bash
Affichage des logs du conteneur : ecblmongodb...
Attaching to ecblmongodb
ecblmongodb        | ------------------------------------------------------------
ecblmongodb        | ETAPE 02 : Stockage des Données Ecobalyse v2.4.0 via MongoDB
ecblmongodb        | ------------------------------------------------------------
ecblmongodb        | VM utilisée, à l'adresse IP / SSH publique : 18.201.106.14
ecblmongodb        | 
ecblmongodb        | about to fork child process, waiting until server is ready for connections.
ecblmongodb        | forked process: 15
ecblmongodb        | child process started successfully, parent exiting
ecblmongodb        | MongoDB shell version v5.0.30
ecblmongodb        | connecting to: mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb
ecblmongodb        | Implicit session: session { "id" : UUID("42c41132-a00e-49d8-8fa8-db77bd20c579") }
ecblmongodb        | MongoDB server version: 5.0.30
ecblmongodb        | ================
ecblmongodb        | Warning: the "mongo" shell has been superseded by "mongosh",
ecblmongodb        | which delivers improved usability and compatibility.The "mongo" shell has been deprecated and will be removed in
ecblmongodb        | an upcoming release.
ecblmongodb        | For installation instructions, see
ecblmongodb        | https://docs.mongodb.com/mongodb-shell/install/
ecblmongodb        | ================
ecblmongodb        | switched to db admin
ecblmongodb        | bye
ecblmongodb        | MongoDB shell version v5.0.30
ecblmongodb        | connecting to: mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb
ecblmongodb        | Implicit session: session { "id" : UUID("e09b9ab9-9e34-46b3-9a77-0c3220c68cc7") }
ecblmongodb        | MongoDB server version: 5.0.30
ecblmongodb        | 
ecblmongodb        | Base De Données MongoDB et fichier 'log' créés avec succès, par le conteneur.
ecblmongodb        | 
```

#### Dockerfile

fichier : Dockerfile.mongo
```bash
# Utilise l'image officielle de MongoDB comme image de base
FROM mongo:5.0

# Définir les variables d'environnement nécessaires
ENV MONGO_INITDB_ROOT_USERNAME=admin
ENV MONGO_INITDB_ROOT_PASSWORD=admin

# Installer Python, pip et le client MongoDB
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv wget gnupg curl

# Ajouter la clé GPG de MongoDB
RUN wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | apt-key add -

# Ajouter le dépôt MongoDB pour la version 5.0
RUN echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-5.0.list

# Mettre à jour les sources et installer le client MongoDB
RUN apt-get update && apt-get install -y mongodb-org-shell

# Créer un environnement virtuel
RUN python3 -m venv /opt/venv

# Activer l'environnement virtuel et installer pymongo et jsonschema
RUN /opt/venv/bin/pip install --upgrade pip
RUN /opt/venv/bin/pip install pymongo
RUN /opt/venv/bin/pip install jsonschema  # Ajout de l'installation de jsonschema

# Copier les scripts d'initialisation et de test dans le conteneur
COPY mongo/init_mongo.js /docker-entrypoint-initdb.d/
COPY mongo/test_mongo.py /app/test_mongo.py
COPY mongo/init_mongo.sh /usr/local/bin/init_mongo.sh
COPY mongo/mongo.conf /etc/mongod.conf
RUN chmod +x /usr/local/bin/init_mongo.sh

# Créer le répertoire de logs
RUN mkdir -p /app/logs

# Copier les fichiers nécessaires dans l'image Docker
COPY mongo/constants1.py /app/
COPY mongo/get_constants1.py /app/

# Ajouter /app au PYTHONPATH
ENV PYTHONPATH="/app"

# Exposer le port MongoDB
EXPOSE 27017

# Définir le point d'entrée pour exécuter le script d'initialisation
ENTRYPOINT ["/usr/local/bin/init_mongo.sh"]
```

### <a name="tdm-07-03" />[Redis](#tdm-07)

#### Dossiers & Répertoires

```bash
.
├── redis
│   ├── Dockerfile.redis
│   ├── constants2.py
│   ├── get_constants2.py
│   ├── init_redis.sh
│   ├── redis.conf
│   └── test_redis.py
.
```

#### Logs du conteneur

conteneur : ecblredis
```bash
Affichage des logs du conteneur : ecblredis...
Attaching to ecblredis
ecblredis          | ----------------------------------------------------------
ecblredis          | ETAPE 02 : Stockage des Données Ecobalyse v2.4.0 via Redis
ecblredis          | ----------------------------------------------------------
ecblredis          | VM utilisée, à l'adresse IP / SSH publique : 18.201.106.14
ecblredis          | 
ecblredis          | 13:C 30 Oct 2024 15:45:48.651 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
ecblredis          | 13:C 30 Oct 2024 15:45:48.651 * Redis version=7.4.1, bits=64, commit=00000000, modified=0, pid=13, just started
ecblredis          | 13:C 30 Oct 2024 15:45:48.651 * Configuration loaded
ecblredis          | 13:M 30 Oct 2024 15:45:48.652 * monotonic clock: POSIX clock_gettime
ecblredis          | 13:M 30 Oct 2024 15:45:48.653 * Running mode=standalone, port=6379.
ecblredis          | 13:M 30 Oct 2024 15:45:48.654 * Server initialized
ecblredis          | 13:M 30 Oct 2024 15:45:48.654 * Ready to accept connections tcp
ecblredis          | 
ecblredis          | Test Redis de récupération JSON : 
ecblredis          | Attendre que le fichier JSON soit créé...
ecblredis          | 
ecblredis          | 
ecblredis          | Base De Données Redis et fichier 'log' créés avec succès, par le conteneur.
ecblredis          |
```

#### Dockerfile

fichier : Dockerfile.redis
```bash
# Utiliser l'image officielle de Redis comme image de base
FROM redis:latest

# Installer procps pour obtenir sysctl et Python avec pip
RUN apt-get update && apt-get install -y procps python3 python3-pip python3-venv curl

# Créer un environnement virtuel
RUN python3 -m venv /opt/venv

# Activer l'environnement virtuel et installer les packages nécessaires
RUN /opt/venv/bin/pip install --upgrade pip
RUN /opt/venv/bin/pip install redis[hiredis]
RUN /opt/venv/bin/pip install cerberus

# Créer le répertoire logs
RUN mkdir -p /app/logs

# Copier les fichiers nécessaires dans l'image Docker
COPY redis/constants2.py /app/
COPY redis/get_constants2.py /app/

# Copier les fichiers de configuration et le script d'initialisation
COPY redis/redis.conf /usr/local/etc/redis/redis.conf
COPY redis/init_redis.sh /usr/local/bin/init_redis.sh
RUN chmod +x /usr/local/bin/init_redis.sh

# Copier le fichier test.py dans le conteneur
COPY redis/test_redis.py /app/test_redis.py

# Définir le point d'entrée pour exécuter le test
ENTRYPOINT ["/usr/local/bin/init_redis.sh"]
CMD ["/opt/venv/bin/python", "/app/test_redis.py"]

```

### <a name="tdm-07-04" />[Flask](#tdm-07)

#### Dossiers & Répertoires

```bash
.
├── flask
│   ├── Dockerfile.flask
│   ├── constants3.py
│   ├── get_constants3.py
│   ├── init_flask.sh
│   ├── mongo_queries.py
│   ├── redis_queries.py
│   ├── requirements.txt
│   ├── stylesheets
│   │   ├── listMongoBDD.css
│   │   └── styles.css
│   ├── templates
│   │   ├── bienvenue.html
│   │   ├── index.html
│   │   └── listMongoBDD.html
│   ├── test_flask.py
│   └── utils.py
.
```

#### Logs du conteneur

conteneur : ecblflask
```bash
Attaching to ecblflask
ecblflask          | --------------------------------------------------------------
ecblflask          | ETAPE 03 : Consommation des Données Ecobalyse v2.4.0 via Flask
ecblflask          | --------------------------------------------------------------
ecblflask          | VM utilisée, à l'adresse IP / SSH publique : 3.252.141.140
ecblflask          | 
ecblflask          | Framework Web Flask démarré. Accessible depuis les adresses : 127.0.0.1:5000/ , ou : 3.252.141.140:5000/
ecblflask          | Fichier 'log' créé avec succès, par le conteneur.
ecblflask          | 
ecblflask          | [2024-10-30 18:35:07,105] INFO in test_flask: Application Flask active.
ecblflask          |  * Serving Flask app 'test_flask.py'
ecblflask          |  * Debug mode: off
ecblflask          | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
ecblflask          |  * Running on all addresses (0.0.0.0)
ecblflask          |  * Running on http://127.0.0.1:5000
ecblflask          |  * Running on http://172.22.0.5:5000
ecblflask          | Press CTRL+C to quit
```

#### Dockerfile

fichier : Dockerfile.flask
```bash
# Utiliser l'image Python slim
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer curl et autres dépendances système
RUN apt-get update && apt-get install -y curl

# Copier le fichier requirements.txt dans l'image Docker
COPY flask/requirements.txt /app/requirements.txt

# Installer les dépendances Python
RUN pip install --no-cache-dir -r /app/requirements.txt 

# Copier tous les fichiers du répertoire flask dans l'image Docker
COPY flask/ /app/

RUN mkdir -p logs

# Rendre le script init_flask.sh exécutable
RUN chmod +x /app/init_flask.sh

# Définir la commande par défaut pour exécuter le script init_flask.sh
CMD ["/app/init_flask.sh"]
```

### <a name="tdm-07-05" />[Dash](#tdm-07)

#### Dossiers & Répertoires

```bash
.
Dash ...
.
```

### <a name="tdm-07-06" />[AirFlow](#tdm-07)

#### Dossiers & Répertoires

```bash
.
AirFlow ...
.
```

## <a name="tdm-06" />[A propos d'Ecobalyse](#debut)
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

[(Retour au début)](#debut)
