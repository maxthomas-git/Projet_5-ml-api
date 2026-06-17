from sqlalchemy import text
from deploiement_modele_ml.database.db_connection import engine



create_table_query = """
CREATE TABLE IF NOT EXISTS prediction_logs (
    id SERIAL PRIMARY KEY,
    
    age INTEGER,
    revenu_mensuel INTEGER,
    nombre_experiences_precedentes INTEGER,
    annee_experience_totale INTEGER,
    annees_dans_l_entreprise INTEGER,
    annees_dans_le_poste_actuel INTEGER,
    augementation_salaire_precedente VARCHAR(10),
    nombre_participation_pee INTEGER,
    nb_formations_suivies INTEGER,
    distance_domicile_travail INTEGER,
    annees_depuis_la_derniere_promotion INTEGER,
    annes_sous_responsable_actuel INTEGER,

    genre VARCHAR(50),
    statut_marital VARCHAR(50),
    departement VARCHAR(100),
    poste VARCHAR(100),
    domaine_etude VARCHAR(100),
    frequence_deplacement VARCHAR(50),
    heure_supplementaires VARCHAR(10),

    niveau_education INTEGER,
    satisfaction_employee_environnement INTEGER,
    note_evaluation_precedente INTEGER,
    satisfaction_employee_nature_travail INTEGER,
    satisfaction_employee_equipe INTEGER,
    satisfaction_employee_equilibre_pro_perso INTEGER,
    note_evaluation_actuelle INTEGER,

    prediction BOOLEAN,
    probabilite_depart FLOAT,
    seuil_utilise FLOAT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

with engine.connect() as conn:
    conn.execute(text(create_table_query))
    conn.commit()

print("Table prediction_logs créée avec succès.")

