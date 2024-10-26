# Datascientest: projet EcoBalyse (Nov. 2024)

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

## <a name="tdm-03" />Mode d'emploi

## <a name="tdm-04" />Etapes du projet

## <a name="tdm-05" />Solution technique

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
