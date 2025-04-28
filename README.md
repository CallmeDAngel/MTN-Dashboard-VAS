# Documentation de l'Application MTN_VAS

## Table des matières

1. Introduction
2. Objectif de l'application
3. Fonctionnalités
4. Architecture de l'application
5. Technologies utilisées
6. Installation
7. Utilisation
8. Récapitulatif
9. Conclusion

## Introduction
L'application MTN_VAS est conçue pour effectuer le scraping de données, réaliser des calculs analytiques, et afficher les résultats sur un tableau de bord. Elle a été développée dans le but d'offrir une plateforme efficace pour la visualisation et l'analyse de données provenant de plusieurs sources.

## Objectif de l'application
L'objectif principal de l'application est de :

- Extraire des données à partir de plusieurs URL en utilisant des scripts de scraping.
- Traiter et analyser les données extraites pour calculer des indicateurs clés de performance (KPI).
- Afficher les résultats dans un tableau de bord convivial, permettant aux utilisateurs de prendre des décisions éclairées basées sur les données.
## Fonctionnalités
L'application offre plusieurs fonctionnalités :

- Scraping de données : Extraction de données de pages web en utilisant Selenium.
- Calcul de KPI : Calcul et stockage des KPI basés sur les données extraites.
- Tableau de bord interactif : Affichage des données et des KPI dans un tableau de bord dynamique et facile à utiliser.
- Notifications : Envoi d'alertes en cas de dépassement de seuils spécifiques pour les KPI.
## Architecture de l'application
L'application est structurée autour des modèles suivants :

- Security : Gestion des niveaux de sécurité des données.
- DataRepository : Stockage des données extraites.
- Scraper : Gestion des informations liées au scraping, telles que les URL sources.
- Plateforme : Gestion des plateformes de données.
- DataSource : Représente les sources de données et leur type.
- DataParser : Traitement des données brutes.
- DataProcessor : Analyse des données et calcul des KPI.
- KPI : Modèle pour stocker les indicateurs de performance.
- Utilisateur, Employe : Gestion des utilisateurs et des permissions.
- Notification : Système d'alerte pour les utilisateurs.
- Dashboard : Structure de l'interface utilisateur.
- Widget : Composants affichant des KPI spécifiques dans le tableau de bord.
## Technologies utilisées
- Django : Framework web pour le développement de l'application.
- Selenium : Outil pour l'automatisation du navigateur, utilisé pour le scraping.
- pandas : Bibliothèque pour la manipulation et l'analyse des données.
- openpyxl : Outil pour travailler avec des fichiers Excel.
- JavaScript/jQuery : Pour la gestion des interactions dans le tableau de bord.
- Chart.js : Bibliothèque pour la création de graphiques et de visualisations de données.
## Installation
Pour installer l'application, suivez ces étapes :
1. Clonez le dépôt :
   - git clone <URL_DU_DEPOT>
   - cd MTN_VAS
2. Créez un environnement virtuel :
   - python -m venv venv
   - source venv/bin/activate   
     venv\Scripts\activate
3. Installez les dépendances :
   - pip install -r requirements.txt
4. Appliquez les migrations de la base de données :
   - python manage.py migrate
5. Lancez le serveur de développement :
   - python manage.py runserver
## Utilisation
1. Accédez à l'application via votre navigateur à l'adresse http://localhost:8000.
2. Connectez-vous avec vos identifiants d'utilisateur.
3. Utilisez l'interface pour configurer les sources de données et les scraping.
4. Consultez le tableau de bord pour visualiser les KPI et les alertes.
## Conclusion
L'application MTN_VAS offre une solution robuste pour l'extraction, l'analyse et la visualisation des données. Grâce à son architecture flexible et à ses fonctionnalités puissantes, elle permet aux utilisateurs de tirer parti des données pour prendre des décisions éclairées.
# Important !!!!!!!!
Le code actuel n'effectue pas vraiment de scraping étant donné qu'il récupère les données sur de fichiers excels. Etant donné le manque de temps, je n'ai pu que faire quelques script de récupération de données mais qui n'ont pas encore été implémenter dans l'application. Ces script se trouve dans le dossier scrript et service de dasboard. Je vous recommande d'intaler Docker pour l'utilisation de Redis afin d'executer les script. J'espère que cela vous sera d'une grande aide. 
# MTN_VAS
