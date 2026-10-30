

# AskCode

**AskCode** est un assistant intelligent conçu pour aider les développeurs à comprendre rapidement un projet existant.

Il analyse le code source, identifie les classes, les méthodes et les fonctions, puis organise ces informations pour faciliter l'exploration d'un dépôt de code.

L'objectif est de pouvoir poser des questions comme :

- Où se trouve la logique d'authentification ?
- Quelle classe gère l'import des articles ?
- Quelles sont les méthodes de ce contrôleur ?
- Comment les différentes parties du projet sont-elles organisées ?

## Fonctionnalités actuelles

- Scan automatique des fichiers Python et PHP.
- Détection des classes, méthodes et fonctions.
- Analyse du code Python avec le module `ast`.
- Analyse du code PHP avec `nikic/PHP-Parser`.
- Génération d'un rapport d'analyse au format JSON.
- Résumé des statistiques du projet.
- Exclusion des dossiers inutiles (`vendor`, `node_modules`, `.venv`, etc.).
- Tests automatisés avec `pytest`.

## Technologies utilisées

| Technologie | Utilisation |
|---|---|
| Python 3.13 | Langage principal |
| PHP | Analyse des fichiers PHP |
| nikic/PHP-Parser | Analyse syntaxique PHP |
| pytest | Tests automatisés |

## Architecture du projet

```text
askcode/
├── php-parser/
│   └── analyze.php
├── scripts/
│   ├── demo_report.py
│   └── demo_summary.py
├── src/
│   └── askcode/
│       ├── scanner.py
│       ├── stats.py
│       ├── analyzer.py
│       ├── php_analyzer.py
│       ├── report.py
│       └── summary.py
├── tests/
├── .gitignore
└── README.md
```

## Installation

Cloner le projet :

```bash
git clone https://github.com/TON-PSEUDO/askcode.git
cd askcode
```

Créer un environnement virtuel :

```bash
python -m venv .venv
```

Activer l'environnement sous Windows :

```powershell
.venv\Scripts\Activate.ps1
```

Installer les dépendances PHP :

```bash
cd php-parser
composer install
cd ..
```

Installer pytest :

```bash
pip install pytest
```

## Utilisation

Analyser un dépôt :

```powershell
python scripts/demo_report.py "CHEMIN_DU_PROJET"
```

Générer un résumé :

```powershell
python scripts/demo_summary.py "CHEMIN_DU_PROJET"
```

Exemple avec un projet Laravel :

```powershell
python scripts/demo_summary.py "C:\laragon\www\cross-origin-newspaper"
```

## Tests

Lancer les tests automatisés :

```bash
pytest -v
```

## Feuille de route

Les prochaines évolutions prévues :

- [ ] Recherche de classes, méthodes et fonctions.
- [ ] Identification des relations entre les composants.
- [ ] Analyse des dépendances et des flux d'exécution.
- [ ] Indexation du code source.
- [ ] Intégration d'un LLM.
- [ ] Mise en place d'un système RAG pour répondre aux questions en langage naturel.
- [ ] Réponses avec références aux fichiers et aux lignes de code.

## Vision du projet

L'objectif final est de transformer AskCode en un assistant capable de comprendre un dépôt de code, d'expliquer son fonctionnement et d'aider les développeurs à naviguer dans des projets qu'ils ne connaissent pas.

**AskCode — Understand your codebase, faster.**

