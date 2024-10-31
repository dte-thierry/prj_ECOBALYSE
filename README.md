<a name="debut" />

<img src="img/PRJ-ECOBALYSE-00-LOGO.png" alt="Logo DataScientest" style="width:250px;height:auto;">

# Datascientest: [projet EcoBalyse](./PRJ-ECOBALYSE-00-FICHE_PROJET.pdf) (Nov. 2024)
Dernière Mise A Jour du Document : Jeu. 31/10/2024 - Version : 0.20

## [Sommaire](#debut)
- [Contexte](#tdm-01)
- [Présentation](#tdm-02)
    - [Etapes du projet](#tdm-02-01)
- [Mode d'emploi](#tdm-03)
    - [Pré-requis](#tdm-03-01)
    - [Lancement](#tdm-03-02)
- [Solution technique](#tdm-05)
    - [Schéma de Principe](#tdm-05-01)
    - [Dossiers & Répertoires](#tdm-05-02)
- [Détails techniques](#tdm-07)
    - [ETL](#tdm-07-01)
    - [MongoDB](#tdm-07-02)
    - [Redis](#tdm-07-03)
    - [Flask](#tdm-07-04)
    - [Dash](#tdm-07-05)
    - [AirFlow](#tdm-07-06)
- [A propos d'Ecobalyse](#tdm-06)

## <a name="tdm-01" />[Contexte](#debut)
Ce projet a été réalisé dans le cadre de la formation de Data Engineer, proposée par :  
<a href="https://datascientest.com/formation-data-engineer" target="_blank">Datascientest et l'Ecole des Mines ParisTech</a>.

L'équipe ayant réalisé ce projet se compose de :
* SERDYUK Alexandra
* BENALLEGUE Anis
* DELIGNE Thierry

## <a name="tdm-02" />[Présentation](#debut)
Basé sur les données, et l'`API` de calcul des impacts environnementaux d'[Ecobalyse v2.4.0](https://ecobalyse.beta.gouv.fr/), ce projet doit permettre : 
- d'obtenir une évaluation de l'impact écologique de textiles courants
- de fournir des recommandations ou des conseils sur des alternatives plus durables

<br />
<img src="img/PRJ-ECOBALYSE-00-IMG2.jpg" alt="Présentation" style="width:750px;height:auto;">

### <a name="tdm-02-01" />[Etapes du projet](#tdm-02)
- Etape 01 : récolte des données - [Extraction](notebook/PRJ-ECOBALYSE-01-ETAPE-01-BASIC_v0-20.ipynb) , [Transformation]((notebook/PRJ-ECOBALYSE-02-ETAPE-01-FULL_v0-20.ipynb))
- Etape 02 : architecture des données
- Etape 03 : consommation des données - [Visualisations](notebook/PRJ-ECOBALYSE-03-ETAPE-03-VISU_v0-20.ipynb) , [Prédictions](notebook/PRJ-ECOBALYSE-04-ETAPE-03-ML_v0-20.ipynb)
- Etape 04 : mise en production
- Etape 05 : automatisation des flux

## <a name="tdm-03" />[Mode d'emploi](#debut)

### <a name="tdm-03-01" />[Pré-requis](#tdm-03)

> **Résumé du(des) script(s) utile(s)**
>
> - `./info.sh -v` # affiche la version du client Docker installé (nota: ./info.sh <b>-?</b> renvoie les options disponibles)
> - `./info.sh -i` # affiche la liste des images Docker présentes 
> - `./info.sh -a` # affiche la liste des conteneurs Docker actifs
> - `./stop.sh` # arrête tous les conteneurs définis dans le fichier docker-compose.yml
> - `./reset.sh` # supprime les données et (ré)initialise toute la configuration du projet

- installer [VS Code](https://code.visualstudio.com/) localement sur votre PC, en fonction de votre système d'exploitation.

- configurer [VS Code](https://code.visualstudio.com/) pour pouvoir accéder, via <i>SSH</i>, à la machine virtuelle DataSientest.

- accéder, puis lancer la machine virtuelle DataScientest, depuis le lien : <br />
*https://learn.datascientest.com/lesson/349/3682*

- au besoin, (ré)installer ou mettre à jour le client **Docker**, depuis le manageur de paquets *apt*, avec les instructions suivantes :

```bash
VERSION_STRING=5:25.0.3-1~ubuntu.20.04~focal
sudo apt-get install docker-ce=$VERSION_STRING docker-ce-cli=$VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin
```

- recopier le dépôt GitHub sur la machine virtuelle, par la commande : <br />
*git clone https://github.com/dte-thierry/prj_ECOBALYSE.git*

- au besoin, utiliser les options du script `./info.sh`, pour afficher les informations du client Docker installé. <br />
(nota: `./info.sh -?` renvoie les options disponibles)

<br />
Puis, depuis le répertoire <i><b>~/prj_ECOBALYSE</i></b> :

- lancer (si nécessaire) le script `./stop.sh` pour arrêter tous les conteneurs.

- lancer le script `./reset.sh` pour supprimer toutes les données (*logs* et *json*), et tous les conteneurs, images, volumes, réseaux inutilisés.

#### Facultatif :

>> **Résumé du(des) script(s) facultatif(s)**
>>
>> - `./start.sh -i` # vérifie l'extraction des Données Ecobalyse (nota: ./start.sh <b>-?</b> renvoie les options disponibles)
>> - `./start.sh` # idem : vérifie l'extraction des Données Ecobalyse

- au besoin, lancer le script `./start.sh -i` pour exécuter une extraction <i>"manuelle"</i> (hors conteneur **Docker**) des données Ecobalyse.

- via [VS Code](https://code.visualstudio.com/), depuis le répertoire */logs*, consulter le contenu du fichier `'manual_webscraping_(date).log'`, pour vérifier le résultat obtenu.

##### Nota :

Vous pouvez lancer le script `./start.sh`, <b>sans aucune option</b>. 

En lançant le script `./start.sh -i`, vous obtiendrez le message d'avertissement :

```bash
--------------------------------------------------------------
ETAPE 01 : Récupération des Données via l'API Ecobalyse v2.4.0
--------------------------------------------------------------
VM en cours, à l'adresse IP / SSH publique : 18.201.106.14

Avertissement:
--------------
L'API d'Ecobalyse est actuellement non finalisée, toujours en cours de développement.
Ce projet se base sur l'API d'Ecobalyse : v2.4.0 pour récupérer les données.
Soyez attentif et vigilant à la récupération des données Ecobalyse obtenues, via l'API.
Consultez dans le répertoire /logs, le fichier .log : (manual|docker)_webscraping_(aaaa-mm-jj_hh-mn).log.
Vérifiez qu'aucune description de textile (colonne 'description') ne soit de type : NaN

DataFrame, fichiers 'log' et 'json' créés avec succès, manuellement.
```

### <a name="tdm-03-02" />[Lancement](#tdm-03)

#### Lancer les services

- lancer le script `setup.sh` pour activer les différents conteneurs et services nécessaires au projet, par la commande : <br />
*./setup.sh*

- via [VS Code](https://code.visualstudio.com/), consulter le contenu des fichiers .log, pour vérifier que l'architecture de stockage `MongoDB` / `Redis` est fonctionnelle. <br />
    - `'docker_webscraping_(date).log'` : pour visualiser l'extraction des données Ecobalyse, par les services
    - `'docker_testmongodb_(date).log'` : pour visualiser l'accès à MongoDB et requêtes initiales, par les services
    - `'docker_testredis_(date).log'` : pour visualiser l'accès à Redis et requêtes initiales, par les services

- lancer le script `info.sh` <b>-logs</b>, pour visualiser les logs des conteneurs actifs, par la commande : <br />
*./info.sh <b>-logs</b>*

##### Nota :

En lançant le script `info.sh` avec l'option `-logs` <i>(nota: ./info.sh <b>-?</b> renvoie les options disponibles)</i>, vous visualiserez les logs des différents conteneurs, par exemple :

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

#### Lancer le Framework Web Flask

Lorsque le Framework Web `Flask` est démarré, on peut y accéder depuis un navigateur Web : <br />

- soit par l'adresse locale : 127.0.0.1:5000/
- soit par l'adresse IP / SSH publique de la VM, par exemple : 3.252.141.140:5000/

La page d'accueil `Flask` s'affiche avec les informations :

```html
Accueil
Bienvenue sur la page d'accueil de votre application Flask !

Pour vérifier le bon fonctionnement de votre application, saisir les adresses :

127.0.0.1:5000/testflask, afin de lister les BDD MongoDB
127.0.0.1:5000/testmongo, afin de vérifier le contenu Ecobalyse de la BDD MongoDB
127.0.0.1:5000/testredis, afin de vérifier le contenu Ecobalyse de la BDD Redis
```

##### Nota :

- lancer le script `info.sh` <b>-logs</b>, permet également d'accéder à Flask, par la commande : <br />
*./info.sh <b>-logs</b>*

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

prj_ECOBALYSE


## <a name="tdm-07" />[Détails techniques](#debut)

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
