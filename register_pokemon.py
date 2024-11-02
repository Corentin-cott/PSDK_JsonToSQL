import csv
import os
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

# Initialisation des variables
db_path = config['bdd_folder'] + '/pokemon.db'
# Toutes tables
pokemon_id = 0
# Table Pokemon
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
    print("Base de données supprimée.")

# Connexion à la base de données SQLite (ou création)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Création de la table pour les Pokémon
cursor.execute('''
    CREATE TABLE Pokemon (
        id INTEGER PRIMARY KEY,
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

# Sauvegarde et fermeture de la connexion
conn.commit()
conn.close()
