import pymysql
import json
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

# Charger les données depuis le fichier JSON
with open('./data/donneesABS.json', 'r', encoding='utf-8') as file:
    donnees_conducteur_vehicule = json.load(file)

# Etablissement de la connexion à la base de données
try:
    connexion = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    print("Connexion réussie !")

    # Création d'un curseur pour exécuter les requêtes SQL
    cursor = connexion.cursor()

    # Insertion des données des véhicules dans la table 'vehicule' en utilisant l'IDconducteur de la table 'conducteur'
    for item in donnees_conducteur_vehicule:
        # Récupération de l'IDconducteur à partir du nom du conducteur
        nom_conducteur = item['CHAUFFEUR']
        sql_select_id_conducteur = "SELECT IDconducteur FROM conducteur WHERE Nom_conducteur = %s"
        cursor.execute(sql_select_id_conducteur, (nom_conducteur,))
        row = cursor.fetchone()
        if row:
            id_conducteur = row[0]
        else:
            print(f"Le conducteur '{nom_conducteur}' n'a pas été trouvé dans la base de données.")
            continue
        
        # Récupération des données du véhicule
        num_interne_tracteur = item.get('N° CAMION', 'NULL') or 'NULL'
        type_vehicule = item.get("TYPE D'ENGIN", 'NULL') or 'NULL'
        marque_vehicule = item.get("MARQUE", 'NULL') or 'NULL'
        plaque_immatriculation = item.get('IMMATRICULATION', 'NULL') or 'NULL'
        num_chassis = item.get('N° SERIE', 'NULL') or 'NULL'
        date_ctr_tech = item.get('controle technique', 'NULL') or 'NULL'
        
        etat_vehicule = item.get('OBSERVATION')
        if etat_vehicule == 'None':
            etat_vehicule = 'Disponible'
        IDSousParc = '18'
        valeurs_a_inserer = {
            "num_interne_tracteur":num_interne_tracteur,
            "type_vehicule":type_vehicule,
            "marque_vehicule":marque_vehicule,
            "plaque_immatriculation":plaque_immatriculation,
            "date_ctr_tech":date_ctr_tech,
            "num_chassis":num_chassis,
            "IDconducteur":id_conducteur,
            "etat_vehicule":etat_vehicule,
            "IDSousParc":IDSousParc
        }
        
        for champ in ["marque_vehicule", "num_interne_tracteur", "num_chassis", "date_ctr_tech"]:
            valeurs_a_inserer[champ] = valeurs_a_inserer[champ] if valeurs_a_inserer[champ] != "null" else None
         # Construction de la requête SQL d'insertion
        champs = ', '.join(valeurs_a_inserer.keys())
        placeholders = ', '.join(['%s'] * len(valeurs_a_inserer))
        sql = f"INSERT INTO vehicule ({champs}) VALUES ({placeholders})"
        
        # Exécution de la requête SQL d'insertion
        cursor.execute(sql, tuple(valeurs_a_inserer.values()))
        print(f"Données du véhicule avec plaque d'immatriculation '{plaque_immatriculation}' insérées avec succès !")

    # Commit des changements
    connexion.commit()
    print("Données insérées avec succès dans la table 'vehicule' !")

    # Fermeture du curseur et de la connexion
    cursor.close()
    connexion.close()
    print("Connexion fermée.")

except Exception as e:
    print(f"Erreur lors de la connexion à la base de données ou de l'insertion des données : {e}")
