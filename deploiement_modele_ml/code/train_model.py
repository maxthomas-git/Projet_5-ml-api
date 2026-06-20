import pandas as pd
from deploiement_modele_ml.database.db_connection import engine
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, FunctionTransformer, OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
import joblib
from sklearn.linear_model import LogisticRegression


# chargement des données
def dataset():
    
   # MODE CI/CD (GitHub Actions)
   if engine is None:
       Evaluation = pd.read_csv("deploiement_modele_ml/data/extrait_eval.csv")
       Sirh = pd.read_csv("deploiement_modele_ml/data/extrait_sirh.csv")
       Sondage = pd.read_csv("deploiement_modele_ml/data/extrait_sondage.csv")
   # MODE LOCAL (PostgreSQL)
   else:
       Evaluation = pd.read_sql('SELECT * FROM "Evaluation"', engine) 
       Sirh = pd.read_sql('SELECT * FROM "Sirh"', engine) 
       Sondage = pd.read_sql('SELECT * FROM "Sondage"', engine)

   # Fusion des tableaux mirh et sondage. On appelle ce nouveau tableau Data
   Data = Sirh.merge(Sondage, left_on="id_employee", right_on="code_sondage")
   Data = Data.drop(columns=["code_sondage"])

   #Fusion des tableaux Data et Evaluation
   Evaluation["eval_number"] = Evaluation["eval_number"].str.replace("E_", "").astype(int)
   Data = Data.merge(Evaluation, left_on="id_employee", right_on = "eval_number")
   Data = Data.drop(columns=["eval_number"])
   return Data


# Nettoyage
def clean_data(Data):
    # suppression de la colonne id_employee
    if "id_employee" in Data.columns:
        Data = Data.drop(["id_employee"], axis = 1)

    # transformations des données de % d'augmentation en entiers (str à l'origine)
    Data["augementation_salaire_precedente"] = Data["augementation_salaire_precedente"].str.replace("%", "", regex = False).astype("int64")

    
    # suppression des variables numériques inutiles
    Data = Data.drop(["nombre_heures_travailless", "nombre_employee_sous_responsabilite"], axis=1, errors="ignore")

    # suppression des variables catégorielles inutiles
    if "ayant_enfants" in Data.columns:
        Data = Data.drop("ayant_enfants", axis = 1)


    # Suppression de la variable niveau_hierarchique_poste très corrélée avec les salaires mensuels
    if "niveau_hierarchique_poste" in Data.columns:
        Data = Data.drop("niveau_hierarchique_poste", axis = 1)
    
    return Data


# Création de nouvelles features
def create_features(Data):

    # temps sans promotion
    Data["temps_sans_promotion"] = (Data["annees_dans_l_entreprise"] - Data["annees_dans_le_poste_actuel"])

    # valorisation experience
    Data["valorisation_experience"] = (Data["revenu_mensuel"] / Data["annee_experience_totale"]).replace([np.inf, -np.inf], 0)

    # valorisation interne
    Data["valorisation_interne"] = (Data["revenu_mensuel"] / Data["annees_dans_l_entreprise"]).replace([np.inf, -np.inf], 0)

    # part de carrière dans l'entreprise
    Data["part_carriere_entreprise"] = (Data["annees_dans_l_entreprise"] / Data["annee_experience_totale"]).fillna(0).replace([np.inf, -np.inf], 0)

    return Data

# création des listes variables

log_cols = ["revenu_mensuel","valorisation_experience", "valorisation_interne"]

standard_cols = ["age","nombre_experiences_precedentes","annee_experience_totale",
                 "annees_dans_l_entreprise","annees_dans_le_poste_actuel",
                 "augementation_salaire_precedente", "nombre_participation_pee",
                 "nb_formations_suivies","distance_domicile_travail", 
                 "annees_depuis_la_derniere_promotion","annes_sous_responsable_actuel",
                 "temps_sans_promotion","part_carriere_entreprise"]

Variable_nominatives = ["genre", "statut_marital", "departement", "poste", "domaine_etude"]

Variables_Ordinales = ["frequence_deplacement"]

Variable_binaire = ['heure_supplementaires']

cat_cols = ['niveau_education','satisfaction_employee_environnement','note_evaluation_precedente',
            'satisfaction_employee_nature_travail','satisfaction_employee_equipe',
            'satisfaction_employee_equilibre_pro_perso','note_evaluation_actuelle']


# Preprocessor
if __name__ == "__main__":
    Data = dataset()
    Data = clean_data(Data)
    Data = create_features(Data)
    y = Data["a_quitte_l_entreprise"].map({"Non":0, "Oui":1}) # cible
    X = Data.loc[:, Data.columns != "a_quitte_l_entreprise"] # features


    log_pipeline = Pipeline([("log", FunctionTransformer(np.log1p)), ("scaler", StandardScaler())])
    numeric_pipeline = Pipeline([("scaler", StandardScaler())])

    preprocessor = ColumnTransformer([("log_num", log_pipeline, log_cols),
                                      ("num", numeric_pipeline, standard_cols), 
                                      ("onehot_cat",OneHotEncoder(drop="first", handle_unknown="ignore"),Variable_nominatives),
                                      ("ordinal_cat", OrdinalEncoder(categories = [["Aucun", "Occasionnel", "Frequent"]]), Variables_Ordinales),
                                      ("binary_cat",OrdinalEncoder(categories=[["Non", "Oui"]]),Variable_binaire),
                                      ("cat", "passthrough", cat_cols)])

    X_preprocessor = preprocessor.fit_transform(X)

    joblib.dump(preprocessor, "preprocessor.pkl")


# Entrainement du modèle
    model = LogisticRegression(class_weight = "balanced", max_iter=5000, C = 0.01, solver = "lbfgs")

    model.fit(X_preprocessor, y)

    joblib.dump(model, "model.pkl")