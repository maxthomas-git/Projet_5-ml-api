import pandas as pd
from fastapi.testclient import TestClient #simuler une requette hppt vers l'api sans lancer un serveur

from code.train_model import dataset # charge les données
from code.train_model import clean_data # nettoie les données
from code.train_model import create_features # créé des variables dérivées

from app.api import app, model, preprocessor # application fastapi, model entrainé, et pipeline de prétraitement


client = TestClient(app) # création d'un client test

# =========================
# TESTS DATA PIPELINE
# =========================

def test_dataset_retourne_dataframe():
    data = dataset()
    assert isinstance(data, pd.DataFrame)


def test_dataset_non_vide():
    data = dataset()
    assert not data.empty


def test_clean_data_retour_dataframe():
    df = pd.DataFrame({
        "id_employee": [1],
        "nombre_heures_travailless": [8],
        "nombre_employee_sous_responsabilite": [1],
        "ayant_enfants": ["non"],
        "niveau_hierarchique_poste": [2],
        "augementation_salaire_precedente": ["10%"]
    })

    result = clean_data(df)

    assert isinstance(result, pd.DataFrame)
    assert "id_employee" not in result.columns


def test_conversion_pourcentage_en_int():
    df = pd.DataFrame({
        "augementation_salaire_precedente": ["10%", "20%", "0%"]
    })

    result = clean_data(df)

    assert list(result["augementation_salaire_precedente"]) == [10, 20, 0]


def test_creation_features():
    df = pd.DataFrame({
        "annees_dans_l_entreprise": [10],
        "annees_dans_le_poste_actuel": [3],
        "revenu_mensuel": [3000],
        "annee_experience_totale": [15]
    })

    result = create_features(df)

    assert "temps_sans_promotion" in result.columns
    assert "valorisation_experience" in result.columns
    assert "valorisation_interne" in result.columns
    assert "part_carriere_entreprise" in result.columns


def test_division_par_zero():
    df = pd.DataFrame({
        "annees_dans_l_entreprise": [0],
        "annees_dans_le_poste_actuel": [0],
        "revenu_mensuel": [1000],
        "annee_experience_totale": [0]
    })

    result = create_features(df)

    assert result["valorisation_experience"].iloc[0] == 0


# =========================
# TEST MODELE (FONCTIONNEL)
# =========================

def test_model_prediction():
    df = pd.DataFrame([{
        "age": 35,
        "revenu_mensuel": 3000,
        "nombre_experiences_precedentes": 2,
        "annee_experience_totale": 10,
        "annees_dans_l_entreprise": 5,
        "annees_dans_le_poste_actuel": 3,
        "augementation_salaire_precedente": "10 %",
        "nombre_participation_pee": 1,
        "nb_formations_suivies": 2,
        "distance_domicile_travail": 12,
        "annees_depuis_la_derniere_promotion": 3,
        "annes_sous_responsable_actuel": 1,
        "genre": "M",
        "statut_marital": "Marié(e)",
        "departement": "Commercial",
        "poste": "Manager",
        "domaine_etude": "Marketing",
        "frequence_deplacement": "Occasionnel",
        "heure_supplementaires": "Oui",
        "niveau_education": 3,
        "satisfaction_employee_environnement": 3,
        "note_evaluation_precedente": 3,
        "satisfaction_employee_nature_travail": 4,
        "satisfaction_employee_equipe": 4,
        "satisfaction_employee_equilibre_pro_perso": 3,
        "note_evaluation_actuelle": 4
    }])
    
    df["augementation_salaire_precedente"] = (df["augementation_salaire_precedente"].str.replace("%", "", regex=False).astype(int))

    df = create_features(df)
    X = preprocessor.transform(df)
    proba = model.predict_proba(X)[0][1]

    assert 0 <= proba <= 1


# =========================
# TEST API FASTAPI
# =========================

def test_api_predict():
    response = client.post("/predict", json={
        "age": 35,
        "revenu_mensuel": 3000,
        "nombre_experiences_precedentes": 2,
        "annee_experience_totale": 10,
        "annees_dans_l_entreprise": 5,
        "annees_dans_le_poste_actuel": 3,
        "augementation_salaire_precedente": "10 %",
        "nombre_participation_pee": 1,
        "nb_formations_suivies": 2,
        "distance_domicile_travail": 12,
        "annees_depuis_la_derniere_promotion": 3,
        "annes_sous_responsable_actuel": 1,
        "genre": "M",
        "statut_marital": "Marié(e)",
        "departement": "Commercial",
        "poste": "Manager",
        "domaine_etude": "Marketing",
        "frequence_deplacement": "Occasionnel",
        "heure_supplementaires": "Oui",
        "niveau_education": 3,
        "satisfaction_employee_environnement": 3,
        "note_evaluation_precedente": 3,
        "satisfaction_employee_nature_travail": 4,
        "satisfaction_employee_equipe": 4,
        "satisfaction_employee_equilibre_pro_perso": 3,
        "note_evaluation_actuelle": 4
    })

    assert response.status_code == 200
    assert "probabilite_depart" in response.json()
    assert "a_quitte_l_entreprise" in response.json()
