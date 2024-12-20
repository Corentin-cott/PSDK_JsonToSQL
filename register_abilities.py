import csv
import re
import sqlite3
import json
import glob

# Lecture du json de config
def load_config(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

config = load_config('./config.json')
print(f'Dossier du projet PSDK : {config['psdk_game_folder']}')
print(f'Dossier du projet PSDK : {config['bdd_folder']}')

# Connexion à la base de données SQLite (ou création)
conn = sqlite3.connect(config['bdd_folder'] + '/abilities.db')
cursor = conn.cursor()

# Création de la table pour les talents
cursor.execute('''CREATE TABLE IF NOT EXISTS abilities (
                    id INTEGER PRIMARY KEY,
                    nameEN TEXT,
                    nameFR TEXT,
                    descEN TEXT,
                    descFR TEXT
                )''')

# Vider la table au cas où elle contient déjà des données
cursor.execute('DELETE FROM abilities')
print('La BDD "abilities.db" à été vidé.')

# Fonction pour insérer un talent dans la BDD
def insert_ability(file_path):
    with open(file_path, 'r') as file:
        ability_data = json.load(file)
        ability_en_name, ability_fr_name, ability_en_desc, ability_fr_desc = get_ability_infos(ability_data['dbSymbol'])
        print(f'Enregistrement "ID : EN : FR" -> {ability_data['id']} : {ability_en_name} : {ability_fr_name}')
        cursor.execute('INSERT INTO abilities (id, nameEN, nameFR, descEN, descFR) VALUES (?, ?, ?, ?, ?)', 
                      (ability_data['id'], ability_en_name, ability_fr_name, ability_en_desc, ability_fr_desc))

# Retire tous les chara spéciaux pour les remplacer par des espaces
def format_ability_name(ability_name):
    # Remplace les caractères indésirables par des espaces
    ability_name = re.sub(r'[_\'-]', ' ', ability_name)
    # Capitalise chaque mot
    ability_name = ' '.join(word.capitalize() for word in ability_name.split())
    return ability_name

# Fonction pour récupérer les noms FR et EN d'un talent à partir du dbSymbol
def get_ability_infos(dbSymbol):
    
    # Initialisation des variables pour la suite
    ability_en_name = format_ability_name(dbSymbol)
    ability_fr_name = ''
    ability_fr_desc = ''
    ability_en_desc = ''
    ability_desc_row = 0
    ability_name_text_file = config['psdk_game_folder'] + '/Data/Text/Dialogs/100004.csv'
    ability_desc_text_file = config['psdk_game_folder'] + '/Data/Text/Dialogs/100005.csv'
    
    # On commence par récupéré le nom FR du talent avec le nom EN (Qui est le nom du fichier)
    try:
        with open(ability_name_text_file, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)  # Première ligne pour les en-têtes
            
            # Trouver les index pour 'en' et 'fr' dans les en-têtes, normalement 0 pour EN et 1 pour FR
            en_index = headers.index('en')
            fr_index = headers.index('fr')
            # Il y a d'autre langues d'enregistré pour PSDK, mais ce programme les ignorera
            
            # Parcourir les lignes pour trouver la correspondance du nom anglais
            rowNumber = 1
            for row in csv_reader:
                rowNumber = rowNumber + 1
                if row[en_index] == ability_en_name:
                    ability_fr_name = row[fr_index]
                    ability_desc_row = rowNumber # Les description sont stocké dans un fichier différent, mais dans le même ordre
                    break  # Sortie de la boucle dès que le nom est trouvé
                
    except FileNotFoundError:
        print("Le fichier de dialogue n'a pas été trouvé.")
    except Exception as e:
        print(f'Erreur lors de la lecture du fichier : {e}')

    # On passe à la récupération des descriptions
    try:
        with open(ability_desc_text_file, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)  # Première ligne pour les en-têtes
            
            # Trouver les index pour 'en' et 'fr' dans les en-têtes, normalement 0 pour EN et 1 pour FR
            en_index = headers.index('en')
            fr_index = headers.index('fr')

            rowNumber = 1
            for row in csv_reader:
                rowNumber = rowNumber + 1
                if rowNumber == ability_desc_row:
                    ability_en_desc = row[en_index]
                    ability_fr_desc = row[fr_index]
                    break  # Sortie de la boucle dès que le nom est trouvé
                
    except FileNotFoundError:
        print("Le fichier de dialogue n'a pas été trouvé.")
    except Exception as e:
        print(f'Erreur lors de la lecture du fichier : {e}')

    return ability_en_name, ability_fr_name, ability_en_desc, ability_fr_desc

# Utiliser glob pour lire tous les fichiers jSON
abilities_file_path = config['psdk_game_folder'] + '/Data/Studio/abilities/*.json'
for file_path in glob.glob(abilities_file_path):
    # print(f'\nLancement de l\'enregistrement du talent "{file_path}"')
    insert_ability(file_path)

# Sauvegarde et fermeture de la connexion
conn.commit()
conn.close()
