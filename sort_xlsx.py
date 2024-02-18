import openpyxl
import json

wb = openpyxl.load_workbook('./data/FLOTTE FBA Au 31-12-2023.xlsx')

sheet = wb['CORSO']

# Créer une liste pour stocker les données
data = []

for row in sheet.iter_rows(values_only=True):
    # Créer un dictionnaire pour stocker les données de chaque ligne
    row_data = {
        "Nom_conducteur":  row[3],
        "telephone_conducteur":  row[4],
        "numero_permis":  row[5],
        "date_delivrance_permis":  row[6],
        # "VALIDITE PERMIS CHAUFFEUR":  row[7],
        "date_expir_permis":  row[8],
    }
    # Ajouter le dictionnaire à la liste des données
    data.append(row_data)

# Fermer le fichier Excel après avoir fini de le lire
wb.close()

# Écrire les données dans un fichier JSON
with open('./data/donneesChoffeur.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

