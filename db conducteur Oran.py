import pymysql
import json
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
import uuid

try:
    # Charger les données depuis le fichier JSON
    with open('./data/donneesORAN.json', 'r', encoding='utf-8') as file:
        conducteurs = json.load(file)

    # Etablissement de la connexion à la base de données avec gestionnaire de contexte
    with pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
    ) as connexion:
        print("Connexion réussie !")

        # Création d'un curseur pour exécuter les requêtes SQL
        with connexion.cursor() as cursor:

            # Vérifier si le nom du conducteur existe déjà dans la table 'conducteur'
            def conducteur_existe(nom):
                sql = "SELECT COUNT(*) FROM conducteur WHERE Nom_conducteur = %s"
                cursor.execute(sql, (nom,))
                return cursor.fetchone()[0] > 0

            # Générer le code UUID en dehors de la boucle
            code_chauffeur = str(uuid.uuid4())[:6]

            # Insertion des données des conducteurs dans la table 'conducteur' si le conducteur n'existe pas encore
            for conducteur in conducteurs:
                nom = conducteur['NOM CHAUFFEUR']
                telephone = conducteur['TEL FBA']
                date_delivrance = conducteur.get('VALIDITE PERMIS A CIRCULER')
                print(f"Insertion des données du conducteur {nom}...")

                # Déterminer quelles valeurs doivent être insérées dans la base de données
                valeurs_a_inserer = {
                    'Nom_conducteur': nom,
                    'telephone_conducteur': telephone,
                    'date_delivrance_permis': date_delivrance,
                    'code_chauffeur': code_chauffeur
                }

                # Vérifier si le conducteur existe déjà
                if not conducteur_existe(nom):
                    # Compléter les valeurs manquantes avec None
                    for champ in ['telephone_conducteur', 'date_delivrance_permis']:
                        valeurs_a_inserer[champ] = valeurs_a_inserer[champ] if valeurs_a_inserer[champ] != "null" else None

                    # Construction de la requête SQL d'insertion
                    champs = ', '.join(valeurs_a_inserer.keys())
                    placeholders = ', '.join(['%s'] * len(valeurs_a_inserer))
                    sql = f"INSERT INTO conducteur ({champs}) VALUES ({placeholders})"

                    # Exécution de la requête SQL d'insertion
                    cursor.execute(sql, tuple(valeurs_a_inserer.values()))
                    print(f"Conducteur '{nom}' ajouté à la base de données.")
                else:
                    print(f"Conducteur '{nom}' existe déjà dans la base de données. Ignoré.")

                # Commit des changements après chaque insertion
                connexion.commit()

        print("Données insérées avec succès dans la table 'conducteur' !")

except pymysql.Error as e:
    print(f"Erreur lors de la connexion à la base de données ou de l'insertion des données : {e}")
