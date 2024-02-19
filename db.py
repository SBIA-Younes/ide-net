import pymysql
import json
# Informations de connexion
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME


# Charger les données depuis le fichier JSON
with open('./data/vehicule.json',  'r', encoding='utf-8') as file:
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
        nom_conducteur = item['Nom_conducteur']
        sql_select_id_conducteur = "SELECT IDconducteur FROM conducteur WHERE Nom_conducteur = %s"
        cursor.execute(sql_select_id_conducteur, (nom_conducteur,))
        row = cursor.fetchone()
        if row:
            id_conducteur = row[0]
        else:
            print(f"Le conducteur '{nom_conducteur}' n'a pas été trouvé dans la base de données.")
            continue

        # Récupération des données du véhicule
        num_interne_tracteur = item['num_interne_tracteur']
        type_vehicule = item['type_vehicule']
        plaque_immatriculation = item['plaque_immatriculation']
        date_ctr_tech = item['date_ctr_tech']
        date_fin_ctr_tech = item['date_fin_ctr_tech']
        num_chassis = item['num_chassis']
        num_interne_remorque = item['num_interne_remorque']
        num_chassis_remorque = item['num_chassis_remorque']
        remorque_immatriculation = item['remorque_immatriculation']

        # Construction de la requête SQL d'insertion du véhicule
        sql_insert_vehicule = """
            INSERT INTO vehicule (
                num_interne_tracteur, type_vehicule, plaque_immatriculation, 
                date_ctr_tech, date_fin_ctr_tech, num_chassis, 
                num_interne_remorque, num_chassis_remorque, remorque_immatriculation, 
                IDconducteur
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        # Exécution de la requête SQL d'insertion du véhicule
        cursor.execute(sql_insert_vehicule, (
            num_interne_tracteur, type_vehicule, plaque_immatriculation, 
            date_ctr_tech, date_fin_ctr_tech, num_chassis, 
            num_interne_remorque, num_chassis_remorque, remorque_immatriculation, 
            id_conducteur
        ))
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