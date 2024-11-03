# PSDK_JsonToSQL 

## Sommaire

- [Introduction](#introduction)
- [PSDK](#psdk)
- [Fonctionnement](#fonctionnement)
- [Contributions](#contributions)

## Introduction

**PSDK JsonToSQL** est simplement un ensemble de scripts écrits en Python qui ont pour objectif de convertir les données JSON (et CSV) de PSDK en tables SQL.

### > En quoi c'est utile ?

Bien que très spécifique, c'est est utile pour afficher les données sur un site Web ou sur une autre interface applicative. Les données de PSDK, modifiables par Studio, sont enregistrées dans plusieurs fichiers différents à des emplacements variés. Par exemple, il existe un fichier JSON pour chaque talent, mais les noms français de ces talents sont tous enregistrés dans un seul fichier CSV à un endroit différent.

Grâce à ces scripts, il est facile et rapide de créer une base de données SQL de toutes ses Fakemon, talents personnalisés, etc., pour les afficher sur un wiki, par exemple !

## PSDK

[Pokemon SDK](https://pokemonworkshop.com/fr/sdk) est un starter kit permettant de créer des fangame Pokémon en utilisant plusieurs outils simple d'utilisation.

> "Contrary to PSP or Essentials, PSDK doesn't use the RGSS. We wrote a graphic engine called LiteRGSS using SFML, which allows a better mastering of the Graphic part of PSDK like adding Shaders, turning some graphic process to C++ side etc...
> 
> - Game Engine : LiteRGSS2 (under Ruby 3.0.1)
> - Default screen size : 320x240 (upscaled to 640x480)
> - Sound : FMOD (Support: Midi, WMA, MP3, OGG, MOD, WAVE)
> - Map Editor
>   - RMXP
>   - Tiled
> - Event Editor
>   - RMXP
> - Database Editor
>   - ~~RubyHost~~ [Pokémon Studio](https://pokemonworkshop.com/fr/studio)
> - Dependencies : SFML, LodePNG, libnsgif, FMOD, OpenGL, sfeMovie, ffmpeg"

## Fonctionnement

Les scripts sont écrits en Python et utilisent les modules suivants :
- [CSV](https://docs.python.org/fr/3/library/csv.html) : Pour lire les fichiers CSV
- [SQLite 3](https://docs.python.org/3/library/sqlite3.html) : Pour créer et insérer les données dans un fichier .db
- [JSON](https://docs.python.org/fr/3/library/json.html) : Pour lire les fichiers JSON
- [Glob](https://docs.python.org/3/library/glob.html) : Pour traiter plusieurs fichier d'un dossier
- [Re](https://docs.python.org/3/library/re.html) & [Unicodedata](https://docs.python.org/3/library/unicodedata) : Pour facilement formatter les charactère spéciaux
- [Os](https://docs.python.org/3/library/os.html) : Pour suprimer le fichier de BDD lors de la création d'un nouveau

## Contributions

[Corentin COTTEREAU](https://github.com/Corentin-cott)
