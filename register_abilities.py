import csv
import sqlite3
import json
import glob

# Connexion à la base de données SQLite (ou création)
conn = sqlite3.connect('./BDD/abilities.db')
cursor = conn.cursor()

# Création de la table pour les talents
cursor.execute('''CREATE TABLE IF NOT EXISTS abilities (
                    id INTEGER PRIMARY KEY,
                    nameEN TEXT,
                    nameFR TEXT
                )''')

# Vider la table au cas où elle contient déjà des données
cursor.execute('DELETE FROM abilities')
print('La BDD "abilities.db" à été vidé.')

# Fonction pour insérer un talent dans la BDD
def insert_ability(file_path):
    with open(file_path, 'r') as file:
        ability_data = json.load(file)
        ability_en_name, ability_fr_name = get_ability_name(ability_data['dbSymbol'])
        print(f'Enregistrement "ID : EN : FR" -> {ability_data['id']} : {ability_en_name} : {ability_fr_name}')
        cursor.execute('INSERT INTO abilities (id, nameEN, nameFR) VALUES (?, ?, ?)', 
                      (ability_data['id'], ability_en_name, ability_fr_name))

# Enlève le caractère '_' pour mettre des espaces a la place
def format_ability_name(dbSymbol):
    ability_name = ''.join(word.capitalize() for word in dbSymbol.split('_'))
    # print('Ability name formatted : ' + ability_name)
    return ability_name

# Fonction pour récupérer les noms FR et EN d'un talent à partir du dbSymbol
def get_ability_name(dbSymbol):
    # print('Récupération des noms FR et EN du talent : ' + dbSymbol)
    ability_text_file = '../pokemon-rlm/Data/Text/Dialogs/100004.csv'
    
    # Initialisation des variables pour les noms
    ability_en_name = format_ability_name(dbSymbol)
    ability_fr_name = ''
    
    # Lecture du fichier CSV qui contient les noms de talents en EN et FR
    try:
        with open(ability_text_file, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)  # Première ligne pour les en-têtes
            
            # Trouver les index pour 'en' et 'fr' dans les en-têtes, normalement 0 pour EN et 1 pour FR
            en_index = headers.index('en')
            fr_index = headers.index('fr')
            # Il y a d'autre langues d'enregistré pour PSDK, mais ce programme les ignorera
            
            # Parcourir les lignes pour trouver la correspondance du nom anglais
            for row in csv_reader:
                if row[en_index] == ability_en_name:
                    ability_fr_name = row[fr_index]
                    break  # Sortie de la boucle dès que le nom est trouvé
                
    except FileNotFoundError:
        print("Le fichier de dialogue n'a pas été trouvé.")
    except Exception as e:
        print(f'Erreur lors de la lecture du fichier : {e}')

    return ability_en_name, ability_fr_name

# Utiliser glob pour lire tous les fichiers jSON
abilities_file_path = '../pokemon-rlm/Data/Studio/abilities/*.json'
for file_path in glob.glob(abilities_file_path):
    # print(f'\nLancement de l\'enregistrement du talent "{file_path}"')
    insert_ability(file_path)

# Sauvegarde et fermeture de la connexion
conn.commit()
conn.close()
