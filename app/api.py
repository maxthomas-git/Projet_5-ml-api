from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import Field
from typing import Literal
import pandas as pd
import joblib
from code.train_model import create_features
from database.db_connection import engine
import os

app = FastAPI()


model = joblib.load("models/model.pkl")
preprocessor = joblib.load("models/preprocessor.pkl")

THRESHOLD = 0.4


# Schéma des données d'entrée (validation)
class InputData(BaseModel):
    age: int = Field(ge=18, le=70)
    revenu_mensuel: int = Field(gt=0)
    nombre_experiences_precedentes: int = Field(ge=0)
    annee_experience_totale: int = Field(ge=0)
    annees_dans_l_entreprise: int = Field(ge=0)
    annees_dans_le_poste_actuel: int = Field(ge=0)
    augementation_salaire_precedente: str = Field(pattern=r"^\d{1,3}\s?%$")
    nombre_participation_pee: int = Field(ge=0)
    nb_formations_suivies: int = Field(ge=0)
    distance_domicile_travail: int = Field(ge=0)
    annees_depuis_la_derniere_promotion: int = Field(ge=0)
    annes_sous_responsable_actuel: int = Field(ge=0)
    genre: Literal["F", "M"]
    statut_marital: Literal['Célibataire', 'Marié(e)', 'Divorcé(e)']
    departement: Literal['Commercial', 'Consulting', 'Ressources Humaines']
    poste: Literal['Cadre Commercial', 'Assistant de Direction', 'Consultant','Tech Lead',
                   'Manager','Senior Manager','Représentant Commercial', 'Directeur Technique', 'Ressources Humaines']
    domaine_etude: Literal['Infra & Cloud','Autre','Transformation Digitale', 
                           'Marketing','Entrepreunariat','Ressources Humaines']
    frequence_deplacement: Literal['Occasionnel', 'Frequent', 'Aucun']
    heure_supplementaires: Literal['Oui', 'Non']
    niveau_education: int = Field(ge=1, le=5)
    satisfaction_employee_environnement: int = Field(ge=1, le=4)
    note_evaluation_precedente: int = Field(ge=1, le=4)
    satisfaction_employee_nature_travail: int = Field(ge=1, le=4)
    satisfaction_employee_equipe: int = Field(ge=1, le=4)
    satisfaction_employee_equilibre_pro_perso: int = Field(ge=1, le=4)
    note_evaluation_actuelle: int = Field(ge=1, le=4)


@app.get("/")
def home():
    return {"message": "API Projet 5 OK"}


@app.post("/predict")
def predict(data: InputData):

    try:
        df = pd.DataFrame([data.model_dump()])

        df["augementation_salaire_precedente"] = (
            df["augementation_salaire_precedente"]
            .str.replace("%", "", regex=False)
            .astype(int)
        )

        df = create_features(df)

        X = preprocessor.transform(df)

        proba = model.predict_proba(X)[0][1]

        prediction = 1 if proba >= THRESHOLD else 0

        return {
            "a_quitte_l_entreprise": bool(prediction),
            "probabilite_depart": float(proba),
            "seuil_utilise": THRESHOLD
        }

    except Exception as e:
        return {"error": str(e)}