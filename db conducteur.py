import pymysql
import json
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
# Informations de connexion



# Charger les données depuis le fichier JSON
with open('./data//conducreur.json', 'r') as file:
    conducteurs = json.load(file)

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

    # Vérifier si le nom du conducteur existe déjà dans la table 'conducteur'
    def conducteur_existe(nom):
        sql = "SELECT COUNT(*) FROM conducteur WHERE Nom_conducteur = %s"
        cursor.execute(sql, (nom,))
        return cursor.fetchone()[0] > 0

    # Insertion des données des conducteurs dans la table 'conducteur' si le conducteur n'existe pas encore
    for conducteur in conducteurs:
        nom = conducteur['Nom_conducteur']
        telephone = conducteur['telephone_conducteur']
        numero_permis = conducteur['numero_permis']
        date_delivrance = conducteur['date_delivrance_permis']
        date_expiration = conducteur['date_expir_permis']
        code_chauffeur = conducteur.get('code_chauffeur', None)  # Récupérer le champ 'code_chauffeur' du conducteur

        # Déterminer quelles valeurs doivent être insérées dans la base de données
        valeurs_a_inserer = {
            'Nom_conducteur': nom,
            'telephone_conducteur': telephone,
            'numero_permis': numero_permis,
            'date_delivrance_permis': date_delivrance,
            'date_expir_permis': date_expiration,
            'code_chauffeur': code_chauffeur  # Inclure le champ 'code_chauffeur'
        }
        
        # Compléter les valeurs manquantes avec NULL
        for champ in ['telephone_conducteur', 'numero_permis', 'date_delivrance_permis', 'date_expir_permis', 'code_chauffeur']:
            if valeurs_a_inserer[champ] is None:
                valeurs_a_inserer[champ] = None

        # Vérifier si le conducteur existe déjà
        if not conducteur_existe(nom):
            # Construction de la requête SQL d'insertion
            champs = ', '.join(valeurs_a_inserer.keys())
            placeholders = ', '.join(['%s'] * len(valeurs_a_inserer))
            sql = f"INSERT INTO conducteur ({champs}) VALUES ({placeholders})"
            
            # Exécution de la requête SQL d'insertion
            cursor.execute(sql, tuple(valeurs_a_inserer.values()))
            print(f"Conducteur '{nom}' ajouté à la base de données.")
        else:
            print(f"Conducteur '{nom}' existe déjà dans la base de données. Ignoré.")

    # Commit des changements
    connexion.commit()
    print("Données insérées avec succès dans la table 'conducteur' !")

    # Fermeture du curseur et de la connexion
    cursor.close()
    connexion.close()
    print("Connexion fermée.")

except Exception as e:
    print(f"Erreur lors de la connexion à la base de données ou de l'insertion des données : {e}")