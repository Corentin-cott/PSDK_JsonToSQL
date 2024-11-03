import csv
import os
import re
import sqlite3
import json
import glob
import time
import unicodedata

# Lecture du json de config
def load_config(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

config = load_config('./config.json')
print(f'Dossier du projet PSDK : {config['psdk_game_folder']}')
print(f'Dossier du projet PSDK : {config['bdd_folder']}')

# Initialisation des variables
pokemon_folder_path = config['psdk_game_folder'] + '/Data/Studio/pokemon/*.json'
db_path = config['bdd_folder'] + '/pokemon.db'
# Toutes tables
pokemon_dexId = 0
# Table Pokemon
nameEN = ''
form = 0
height = 0
weight = 0
type1 = ''
type2 = ''
baseHp = 0
baseAtk = 0
baseDfe = 0
baseSpd = 0
baseAts = 0
baseDfs = 0
evGivenHp = 0
evGivenAtk = 0
evGivenDfe = 0
evGivenSpd = 0
evGivenAts = 0
evGivenDfs = 0
experienceType = ''
baseExperience = 0
baseLoyalty = 0
catchRate = 0
femaleRate = 0
hatchSteps = 0
babyDbSymbol = ''
babyForm = 0
# Table Evolutions
evo_dbSymbol = ''
evo_form = 0
conditionType = ''
conditionValue = 0
# Table Abilities
abilityOne = ''
abilityTwo = ''
abilityHidden = ''
# Table BreedGroups
breedGroupOne = 0
breedGroupTwo = 0

# Suppression de la base de données si elle existe
if os.path.exists(db_path):
    os.remove(db_path)
    print("\nUn ancienne base de donnée à été trouver, elle va être supprimée.\n")
    time.sleep(2.5)

# Connexion à la base de données SQLite (ou création)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Retire tous les chara spéciaux pour les remplacer par des espaces
def format_text(text):
    # Supprime les accents
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')  # Enlève les marques diacritiques (accents)
    
    # Remplace tous les caractères non alphanumériques par rien (supprime-les)
    text = re.sub(r"[^a-zA-Z0-9]", "", text)
    
    # Met en minuscules
    return text.lower()

# Création de la table pour les Pokémon
cursor.execute('''
    CREATE TABLE Pokemon (
        id INTEGER PRIMARY KEY,
        dexId INT NOT NULL,
        nameEN VARCHAR(20),
        nameFR VARCHAR(20),
        descEN TEXT,
        descFR TEXT,
        form INT NOT NULL,
        height DECIMAL(3,1) NOT NULL,
        weight DECIMAL(4,1) NOT NULL,
        type1 VARCHAR(20) NOT NULL,
        type2 VARCHAR(20),
        baseHp INT NOT NULL,
        baseAtk INT NOT NULL,
        baseDfe INT NOT NULL,
        baseSpd INT NOT NULL,
        baseAts INT NOT NULL,
        baseDfs INT NOT NULL,
        evGivenHp INT DEFAULT 0,
        evGivenAtk INT DEFAULT 0,
        evGivenDfe INT DEFAULT 0,
        evGivenSpd INT DEFAULT 0,
        evGivenAts INT DEFAULT 0,
        evGivenDfs INT DEFAULT 0,
        experienceType INT NOT NULL,
        baseExperience INT NOT NULL,
        baseLoyalty INT NOT NULL,
        catchRate INT NOT NULL,
        femaleRate INT,
        hatchSteps INT NOT NULL,
        babyDbSymbol VARCHAR(20),
        babyForm INT
    );
''')

# Fonction pour récupéré le nom FR d'un Pokémon à partir de son nom EN
def get_pokemon_nameFR(nameEN):
    # Initialisation des variables
    pokemon_name_text_file = config['psdk_game_folder'] + '/Data/Text/Dialogs/100000.csv'
    nameFR = ''
    pokemon_desc_row = 0
    
    # Lecture du fichier CSV qui contient les noms de Pokémon
    try:
        with open(pokemon_name_text_file, mode='r', encoding='utf-8') as file:
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
                # print(f'{rowNumber} | ROW = {row[en_index]} / RECH = {nameEN}')
                if format_text(row[en_index]) == format_text(nameEN):
                    nameFR = row[fr_index]
                    pokemon_desc_row = rowNumber
                    break  # Sortie de la boucle dès (que le nom est trouvé
                
    except FileNotFoundError:
        print("Le fichier de dialogue n'a pas été trouvé.")
    except Exception as e:
        print(f'Erreur lors de la lecture du fichier : {e}')

    return nameFR, pokemon_desc_row

# Fonction pour récupéré les descriptions EN et FR d'un Pokémon à partir de la ligne de ses textes
def get_pokemon_descs(pokemon_desc_row):
    # Initialisation des variables
    pokemon_desc_text_file = config['psdk_game_folder'] + '/Data/Text/Dialogs/100002.csv'
    pokemon_en_desc = ''
    pokemon_fr_desc = ''

    # On passe à la récupération des descriptions
    try:
        with open(pokemon_desc_text_file, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)  # Première ligne pour les en-têtes
            
            # Trouver les index pour 'en' et 'fr' dans les en-têtes, normalement 0 pour EN et 1 pour FR
            en_index = headers.index('en')
            fr_index = headers.index('fr')

            rowNumber = 1
            for row in csv_reader:
                rowNumber = rowNumber + 1
                if rowNumber == pokemon_desc_row:
                    pokemon_en_desc = row[en_index]
                    pokemon_fr_desc = row[fr_index]
                    break  # Sortie de la boucle dès que le nom est trouvé
                
    except FileNotFoundError:
        print("Le fichier de dialogue n'a pas été trouvé.")
    except Exception as e:
        print(f'Erreur lors de la lecture du fichier : {e}')

    if not pokemon_en_desc:
        pokemon_en_desc = 'No description'
    if not pokemon_fr_desc:
        pokemon_fr_desc = 'Pas de description'

    return pokemon_en_desc, pokemon_fr_desc

# Fonction d'insertion d'un Pokémon
def insert_pokemon(pokemon_dexId, nameEN, form, height, weight, type1, type2, baseHp, baseAtk, baseDfe, baseSpd, baseAts, baseDfs, evGivenHp, evGivenAtk, evGivenDfe, evGivenSpd, evGivenAts, evGivenDfs, experienceType, baseExperience, baseLoyalty, catchRate, femaleRate, hatchSteps, babyDbSymbol, babyForm):
    # Récupération du nom FR
    nameFR, pokemon_desc_row = get_pokemon_nameFR(nameEN)
    # Récupération des description EN et FR
    descEN, descFR = get_pokemon_descs(pokemon_desc_row)
    print(f'Insertion du Pokémon {nameEN} : Dex {pokemon_dexId}')
    # Préparation de la requête SQL pour insérer un Pokémon
    cursor.execute('''
        INSERT INTO Pokemon (
            dexId, nameEN, nameFR, descEN, descFR, form, height, weight, type1, type2, baseHp, baseAtk, baseDfe, baseSpd, baseAts, baseDfs,
            evGivenHp, evGivenAtk, evGivenDfe, evGivenSpd, evGivenAts, evGivenDfs, experienceType, baseExperience,
            baseLoyalty, catchRate, femaleRate, hatchSteps, babyDbSymbol, babyForm
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        pokemon_dexId, nameEN, nameFR, descEN, descFR, form, height, weight, type1, type2, baseHp, baseAtk, baseDfe, baseSpd, baseAts, baseDfs,
        evGivenHp, evGivenAtk, evGivenDfe, evGivenSpd, evGivenAts, evGivenDfs, experienceType, baseExperience,
        baseLoyalty, catchRate, femaleRate, hatchSteps, babyDbSymbol, babyForm
    ))

    # Sauvegarde des modifications
    conn.commit()

# Création de la table pour les évolutions de Pokémon
cursor.execute('''
    CREATE TABLE Evolutions (
        id INTEGER PRIMARY KEY,
        pokemon_id INT,
        dbSymbol VARCHAR(20) NOT NULL,
        form INT NOT NULL,
        conditionType VARCHAR(20),
        conditionValue INT,
        FOREIGN KEY (pokemon_id) REFERENCES Pokemon(id)
    );
''')

# Création de la table pour les talents de Pokémon
cursor.execute('''
    CREATE TABLE Abilities (
        id INTEGER PRIMARY KEY,
        pokemon_id INT,
        abilityOne VARCHAR(30) NOT NULL,
        abilityTwo VARCHAR(30) NOT NULL,
        abilityHidden VARCHAR(30) NOT NULL,
        FOREIGN KEY (pokemon_id) REFERENCES Pokemon(id)
    );
''')

# Création de la table pour les groupe d'oeuf de Pokémon
cursor.execute('''
    CREATE TABLE BreedGroups (
        id INTEGER PRIMARY KEY,
        pokemon_id INT,
        breedGroupOne INT,
        breedGroupTwo INT,
        FOREIGN KEY (pokemon_id) REFERENCES Pokemon(id)
    );
''')

# Utiliser glob pour lire tous les fichiers jSON de Pokémon
file_count = 0
for file_path in glob.glob(pokemon_folder_path):
    file_count = file_count + 1
    with open(file_path, 'r') as file:
        pokemon_data = json.load(file)
        # Insertions dans la Table Pokemon
        for form in pokemon_data['forms']:
            insert_pokemon(
                pokemon_data['id'],
                pokemon_data['dbSymbol'],
                form['form'],
                form['height'],
                form['weight'],
                form['type1'],
                form['type2'],
                form['baseHp'],
                form['baseAtk'],
                form['baseDfe'],
                form['baseSpd'],
                form['baseAts'],
                form['baseDfs'],
                form['evHp'],
                form['evAtk'],
                form['evDfe'],
                form['evSpd'],
                form['evAts'],
                form['evDfs'],
                form['experienceType'],
                form['baseExperience'],
                form['baseLoyalty'],
                form['catchRate'],
                form['femaleRate'],
                form['hatchSteps'],
                form['babyDbSymbol'],
                form['babyForm']
            )

# Sauvegarde et fermeture de la connexion
conn.commit()
conn.close()
