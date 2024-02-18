import openpyxl
import json

wb = openpyxl.load_workbook('./FLOTTE FBA Au 31-12-2023.xlsx')

sheet = wb['CORSO']

# Créer une liste pour stocker les données
data = []

for row in sheet.iter_rows(values_only=True):
    # Créer un dictionnaire pour stocker les données de chaque ligne
    row_data = {
        "N°": row[0],
        # "N° INTERNE TRACTEUR": row[1],
        # "TAG": row[2],
        "NOM CHAUFFEUR": row[3],
        "TEL FBA": row[4],
        "N° PERMIS CHAUFFEUR": row[5],
        "Permis délivré le": row[6],
        "VALIDITE PERMIS CHAUFFEUR": row[5],
        # "MATRICULE TRACTEUR": row[6],
        "age": row[7],
        "Date début CT": row[8],
        # "VALIDITE CONTRÔLE TECHNIQUE": row[9],
        "VALIDITE PERMIS A CIRCULER": row[10],
        # "Jours Restants PAC": row[11],
        # "NUMERO DE CHASSIS TRACTEUR": row[12],
        # "NOMBRE SANGLE": row[13],
        # "N° Interne Extincteur": row[14],
        # "VALIDITE EXTINCTEUR": row[15],
        # "Experation Extincteur Dans": row[16],
        # "TRIANGLE": row[17],
        # "BOITE A PHARMACIE": row[18],
        # "CALE DE ROUE": row[19],
        # "CLE CABINE": row[20],
        # "Clé de Roue": row[21],
        # "CRIQUE": row[22],
        # "Clé 27": row[23],
        # "NUMERO INTERNE REMORQUE": row[24],
        # "MATRICULE REMORQUE": row[25],
    }
    # Ajouter le dictionnaire à la liste des données
    data.append(row_data)

# Fermer le fichier Excel après avoir fini de le lire
wb.close()

# Écrire les données dans un fichier JSON
with open('./data/donneesChoffeur.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

# Obtenir le nombre de colonnes dans la feuille de calcul
# num_columns = sheet.max_column

# # Boucler à travers chaque ligne et colonne pour récupérer les données
# for row in sheet.iter_rows(values_only=True):
#     # Créer un dictionnaire pour stocker les données de chaque ligne
#     row_data = {}
#     for col_idx in range(num_columns):
#         # Utiliser l'en-tête de colonne comme clé dans le dictionnaire
#         col_header = sheet.cell(row=1, column=col_idx + 1).value
#         row_data[col_header] = row[col_idx]
#     # Ajouter le dictionnaire à la liste des données
#     data.append(row_data)

# # Fermer le fichier Excel après avoir fini de le lire
# wb.close()

# # Écrire les données dans un fichier JSON
# with open('donnees_2.json', 'w', encoding='utf-8') as json_file:
#     json.dump(data, json_file, indent=4, ensure_ascii=False)