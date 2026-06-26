
# Projet 5 - API de prédiction de départ des employés

##  Présentation

Ce projet a pour objectif  développer une API de machine learning permettant de prédire la probabilité de départ d’un employé à partir de données RH.

Le modèle est entraîné sur des données issues de plusieurs sources (SIRH, sondages, évaluations) et exposé via une API FastAPI.


Ce projet permet d’aider les équipes RH à :

- Anticiper les départs d’employés
- Identifier les facteurs de risque
- Prendre des décisions basées sur la data

## Type de modèle utilisé

Après une validation croisée, et une optimisation des hyperparapètres, le modèle le plus adapté pour répondre à la problématique,est une **régression logistique (Logistic Regression)**.  
Etant donné qu'un départ non anticipé a un cout plus important pour l'netreprise qu'un faux départ, la métrique qui a étée privilégiée, est le rappel.  
Les performances du modèle sont un rappel de 81%, pour une précision de 25%.  
L'ensemble des démarches ayant permis de choisir ce modèle est détaillé dans le notebook ci-joint.  

## Justification des choix techniques

### FastAPI
FastAPI a été choisi pour développer l’API car il est :  
- simple à intégrer avec des modèles de machine learning  
- adapté aux projets de production  

Il permet également une validation automatique des données grâce à Pydantic.

---

###  Scikit-learn
Scikit-learn est utilisé pour :  
- la construction du pipeline de preprocessing  
- l’entraînement du modèle de classification  

Il est adapté aux problèmes de classification supervisée.

---

###  PostgreSQL
PostgreSQL est utilisé pour :  
- stocker les données structurées (SIRH, sondages, évaluations)  
- enregistrer les prédictions du modèle  

C’est une base fiable, scalable.

---

###  Pandas
Pandas est utilisé pour :  
- la manipulation des datasets  
- le nettoyage et la fusion des sources de données  
- la préparation des données pour le modèle

## Architecture du projet

Le projet est organisé selon une architecture modulaire séparant les différentes étapes du pipeline ML :  




├── app/  
│ └── api.py  
│ → API FastAPI  
│  
├── code/  
│ └── train_model.py  
│ → Pipeline complet de machine learning :  
│ - chargement des données  
│ - nettoyage  
│ - feature engineering  
│ - entraînement du modèle  
│  
├── database/  
│ ├── db_connection.py  
│ → Connexion PostgreSQL (mode local)  
│ ├── import_csv.py  
│ → Import des données CSV en base  
│ ├──`create_prediction_tables.py`  
│  → Création d'une base de données récoltant les données testées ainsi que leur résultats  
│  
├── models/  
│ → Contient les modèles entraînés :  
│ - model.pkl  
│ - preprocessor.pkl  
│  
├── data/  
│ → Données sources utilisées en mode CI/CD (CSV)  
│  
├── tests/  
│ → Tests unitaires et fonctionnels (pytest)  
│  
└── .github/workflows/  
→ Pipeline CI/CD GitHub Actions  

## UML de la base de données(DB diagramme)

Ce diagramme représente la structure des tables utilisées dans le projet.

 [Voir le diagramme UML](docs/UML.pdf)


## Installation

### 1. Installer les dépendances avec uv

```bash
uv sync
```

### 2. Activer l’environnement


```bash
source .venv/bin/activate
```

## Définition d'une variable d'environnement en local


```bash
export ENV=local
```


## Base de données (PostgreSQL)

Le projet utilise PostgreSQL en local pour stocker les données.

### Création de la base de données

- Ouvrir PostgreSQL
```bash
sudo -u postgres psql
```
- Créer un utilisateur
```sql
CREATE USER attrition_user WITH PASSWORD 'Attrition2026!';
```
- Créer la base de données
```sql
CREATE DATABASE employes_db OWNER attrition_user;
```
- Donner les droits
```sql
GRANT ALL PRIVILEGES ON DATABASE employes_db TO attrition_user;
```

### Connection à la base de données


```bash
python -m database.db_connection
```
### Chargement des données dans la base de donnée postgresql

```bash
python -m database.import_csv
```
### Création de la base de données qui récupèrera les données testées

```bash
python -m database.create_prediction_tables
```

## Chargement, Nettoyage, prétraitement et entrainement du modèle

```bash
python -m code.train_model
```

## Lancer l’API
```bash
uvicorn app.api:app --reload
```
Accès :  
- http://127.0.0.1:8000  
- http://127.0.0.1:8000/docs

##  Endpoint /predict (Exemple)

Entrée : données employé (JSON)

{
  "age": 24,
  "revenu_mensuel": 2700,
  "nombre_experiences_precedentes": 1,
  "annee_experience_totale": 5,
  "annees_dans_l_entreprise": 3,
  "annees_dans_le_poste_actuel": 2,
  "augementation_salaire_precedente": "25 %",
  "nombre_participation_pee": 0,
  "nb_formations_suivies": 1,
  "distance_domicile_travail": 2,
  "annees_depuis_la_derniere_promotion": 2,
  "annes_sous_responsable_actuel": 2,
  "genre": "F",
  "statut_marital": "Célibataire",
  "departement": "Commercial",
  "poste": "Cadre Commercial",
  "domaine_etude": "Infra & Cloud",
  "frequence_deplacement": "Occasionnel",
  "heure_supplementaires": "Oui",
  "niveau_education": 4,
  "satisfaction_employee_environnement": 4,
  "note_evaluation_precedente": 3,
  "satisfaction_employee_nature_travail": 4,
  "satisfaction_employee_equipe": 4,
  "satisfaction_employee_equilibre_pro_perso": 4,
  "note_evaluation_actuelle": 4
}

Sortie :

{
  "a_quitte_l_entreprise": true,
  "probabilite_depart": 0.47021598756070654,
  "seuil_utilise": 0.4
}

## Tests

Lancer les tests :  

```bash
python -m pytest
```

## CI/CD
  
Le projet utilise GitHub Actions pour :  
- installer les dépendances  
- exécuter les tests automatiquement  
- valider chaque push sur main  
- valider chaque pull request sur main  
- déployer automatiquement l'application sur le Space Hugging Face après validation des tests  
- copier les fichiers nécessaires (application, modèles et configuration) vers le dépôt du Space Hugging Face  
- effectuer automatiquement un commit et un push vers le dépôt Hugging Face pour déclencher le redéploiement  

Workflow :  
.github/workflows/tests.yml

##  Maintenance et mise à jour du modèle

###  Mise à jour des données
Les données utilisées pour entraîner le modèle proviennent de trois sources :  
- extrait_sirh  
- extrait_sondage  
- extrait_eval  

Ces données peuvent être mises à jour régulièrement en relançant le script :  

```bash
python -m database.import_csv
```
### Réentrainement du model

```bash
python -m code.train_model
```

### Mise à jour en production

Lorsqu’un nouveau modèle est généré :

- remplacer les fichiers dans models/ (les fichiers .pkl)  
- redémarrer l’API FastAPI:
```bash
uvicorn app.api:app --reload
```

## URL du deploiement

Le dépôt Hugging Face Space:  

https://huggingface.co/spaces/maximilien777/Projet5_ml_api

L'API est déployée sur Hugging Face Spaces et sa documentation Swagger est disponible à l'adresse :  

https://maximilien777-projet5-ml-api.hf.space/docs  

## Auteur  
Maximilien THOMAS  
Projet réalisé dans le cadre d’une formation Data Scientist.
