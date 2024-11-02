import csv
import re
import sqlite3
import json
import glob

# Connexion à la base de données SQLite (ou création)
conn = sqlite3.connect('./BDD/moves.db')
cursor = conn.cursor()

# Création de la table pour les attaques
cursor.execute('''CREATE TABLE IF NOT EXISTS moves (
                    id INTEGER PRIMARY KEY,
                    en_name TEXT,
                    fr_name TEXT,
                    type TEXT,
                    power INTEGER,
                    accuracy INTEGER,
                    PP INTEGER,
                    category TEXT,
                    movecriticalRate INTEGER,
                    priority INTEGER,
                    isAuthentic BOOLEAN,
                    isBallistics BOOLEAN,
                    isBite BOOLEAN,
                    isBlocable BOOLEAN,
                    isCharge BOOLEAN,
                    isDance BOOLEAN,
                    isDirect BOOLEAN,
                    isDistance BOOLEAN,
                    isEffectChance BOOLEAN,
                    isGravity BOOLEAN,
                    isHeal BOOLEAN,
                    isKingRockUtility BOOLEAN,
                    isMagicCoatAffected BOOLEAN,
                    isMental BOOLEAN,
                    isMirrorMove BOOLEAN,
                    isNonSkyBattle BOOLEAN,
                    isPowder BOOLEAN,
                    isPulse BOOLEAN,
                    isPunch BOOLEAN,
                    isRecharge BOOLEAN,
                    isSnatchable BOOLEAN,
                    isSoundAttack BOOLEAN,
                    isUnfreeze BOOLEAN,
                    battleEngineAimedTarget TEXT,
                    battleStageMod TEXT,
                    moveStatus TEXT,
                    effectChance INTEGER,
                    isSlicingAttack BOOLEAN,
                    isWind BOOLEAN
                );''')

# Vider la table au cas où elle contient déjà des données
cursor.execute('DELETE FROM moves')
print('La BDD "moves.db" à été vidé.')

# Fonction pour insérer une attaque dans la BDD
def insert_move(file_path):
    with open(file_path, 'r') as file:
        move_data = json.load(file)
        # Récupération des nom en et fr de l'attaque
        move_en_name, move_fr_name = get_move_name(move_data['dbSymbol'])
        # Vérification que battleStageMod & moveStatus ne sont pas vide
        battleStageMod = ''
        if move_data['battleStageMod']: battleStageMod = move_data['battleStageMod']
        else: battleStageMod = '/'
        moveStatus = ''
        if move_data['moveStatus']: moveStatus = move_data['moveStatus']
        else: moveStatus = '/'
        print(f'Enregistrement "ID : EN : FR" -> {move_data["id"]} : {move_en_name} : {move_fr_name}')
        
        # Insérer les données dans la table "moves"
        cursor.execute('''
            INSERT INTO moves (
                id, en_name, fr_name, type, power, accuracy, PP, category,
                movecriticalRate, priority, isAuthentic, isBallistics,
                isBite, isBlocable, isCharge, isDance, isDirect,
                isDistance, isEffectChance, isGravity, isHeal,
                isKingRockUtility, isMagicCoatAffected, isMental,
                isMirrorMove, isNonSkyBattle, isPowder, isPulse,
                isPunch, isRecharge, isSnatchable, isSoundAttack,
                isUnfreeze, battleEngineAimedTarget, battleStageMod,
                moveStatus, effectChance, isSlicingAttack, isWind
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            move_data['id'],
            move_en_name,
            move_fr_name,
            move_data['type'],
            move_data['power'],
            move_data['accuracy'],
            move_data['pp'],
            move_data['category'],
            move_data['movecriticalRate'],
            move_data['priority'],
            move_data['isAuthentic'],
            move_data['isBallistics'],
            move_data['isBite'],
            move_data['isBlocable'],
            move_data['isCharge'],
            move_data['isDance'],
            move_data['isDirect'],
            move_data['isDistance'],
            move_data['isEffectChance'],
            move_data['isGravity'],
            move_data['isHeal'],
            move_data['isKingRockUtility'],
            move_data['isMagicCoatAffected'],
            move_data['isMental'],
            move_data['isMirrorMove'],
            move_data['isNonSkyBattle'],
            move_data['isPowder'],
            move_data['isPulse'],
            move_data['isPunch'],
            move_data['isRecharge'],
            move_data['isSnatchable'],
            move_data['isSoundAttack'],
            move_data['isUnfreeze'],
            move_data['battleEngineAimedTarget'],
            json.dumps(battleStageMod),
            json.dumps(moveStatus),
            move_data['effectChance'],
            move_data['isSlicingAttack'],
            move_data['isWind']
        ))

# Retire tous les chara spéciaux pour les remplacer par des espaces
def format_move_name(move_name):
    # Remplace les caractères indésirables par des espaces
    move_name = re.sub(r'[_\'-]', ' ', move_name)
    # Capitalise chaque mot
    move_name = ' '.join(word.capitalize() for word in move_name.split())
    return move_name

# Fonction pour récupérer les noms FR et EN d'une attaque à partir du dbSymbol
def get_move_name(dbSymbol):
    # print('Récupération des noms FR et EN de l'attaque : ' + dbSymbol)
    move_text_file = '../pokemon-rlm/Data/Text/Dialogs/100006.csv'
    
    # Initialisation des variables pour les noms
    move_en_name = format_move_name(dbSymbol)
    move_fr_name = ''
    
    # Lecture du fichier CSV qui contient les noms d'attaque en EN et FR
    try:
        with open(move_text_file, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)  # Première ligne pour les en-têtes
            
            # Trouver les index pour 'en' et 'fr' dans les en-têtes, normalement 0 pour EN et 1 pour FR
            en_index = headers.index('en')
            fr_index = headers.index('fr')
            # Il y a d'autre langues d'enregistré pour PSDK, mais ce programme les ignorera
            
            # Parcourir les lignes pour trouver la correspondance du nom anglais
            for row in csv_reader:
                if format_move_name(row[en_index]) == move_en_name:
                    move_fr_name = row[fr_index]
                    break  # Sortie de la boucle dès (que le nom est trouvé
                
    except FileNotFoundError:
        print("Le fichier de dialogue n'a pas été trouvé.")
    except Exception as e:
        print(f'Erreur lors de la lecture du fichier : {e}')

    return move_en_name, move_fr_name

# Utiliser glob pour lire tous les fichiers jSON
abilities_file_path = '../pokemon-rlm/Data/Studio/moves/*.json'
for file_path in glob.glob(abilities_file_path):
    # print(f'\nLancement de l\'enregistrement de l'attaque "{file_path}"')
    insert_move(file_path)

# Sauvegarde et fermeture de la connexion
conn.commit()
conn.close()
