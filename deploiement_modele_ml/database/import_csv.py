import pandas as pd
from deploiement_modele_ml.database.db_connection import engine

Evaluation = pd.read_csv("deploiement_modele_ml/data/extrait_eval.csv")
Sirh = pd.read_csv("deploiement_modele_ml/data/extrait_sirh.csv")
Sondage = pd.read_csv("deploiement_modele_ml/data/extrait_sondage.csv")

Evaluation.to_sql("Evaluation", engine, if_exists = "replace", index =False)
Sirh.to_sql("Sirh", engine, if_exists = "replace", index =False)
Sondage.to_sql("Sondage", engine, if_exists = "replace", index =False)