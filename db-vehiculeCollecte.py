import pymysql
import json
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

# Charger les données depuis le fichier JSON
with open('./data/donneesCollecte.json', 'r', encoding='utf-8') as file:
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
        num_interne_tracteur = item.get('N° INT', 'NULL') or 'NULL'
        IDconducteur = item.get("id_conducteur", 'NULL') or 'NULL'
        type_vehicule = 'TRACTEUR'
        plaque_immatriculation = item.get('TRACTEUR', 'NULL') or 'NULL'
        num_chassis = item.get('NUMERO DE CHASSIS', 'NULL') or 'NULL'
        date_ctr_tech = item.get('contrôle technic', 'NULL') or 'NULL'
        remorque_immatriculation = item.get('CITERNE', 'NULL') or 'NULL'
        num_chassis_remorque = item.get('NUM CHASSIS', 'NULL') or 'NULL'
        type_remorque = 'CITERNE'
        IDSousParc = '17'
        valeurs_a_inserer = {
            "num_interne_tracteur":num_interne_tracteur,
            "IDconducteur":id_conducteur,
            "type_vehicule":type_vehicule,
            "plaque_immatriculation":plaque_immatriculation,
            "num_chassis":num_chassis,
            "date_ctr_tech":date_ctr_tech,
            'remorque_immatriculation':remorque_immatriculation,
            'num_chassis_remorque':num_chassis_remorque,
            'type_remorque':type_remorque,
            "IDSousParc":IDSousParc
        }
        
        for champ in ['num_interne_tracteur',"IDconducteur","type_vehicule","plaque_immatriculation","num_chassis","date_ctr_tech", 'remorque_immatriculation','num_chassis_remorque','type_remorque',"IDSousParc"]:
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
