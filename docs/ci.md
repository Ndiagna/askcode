# Documentation technique de la CI

## Objectif et déclenchement

Le workflow GitHub Actions `.github/workflows/ci.yml` s’exécute sur les
`push` et les `pull_request` ciblant `develop` ou `master`. Il utilise des
actions composites locales dans `.github/actions/` pour nommer et isoler
logiquement les phases, sans créer un runner ni réinstaller les dépendances
pour chaque phase.

Le pipeline suit cet ordre :

1. **Prepare** — initialise Python et PHP, restaure les caches et installe les
   dépendances une fois.
2. **Validate** — affiche et valide les métadonnées de PR, vérifie les
   dépendances et signale les versions obsolètes.
3. **Code quality** — exécute formatage, lint, typage et contrôles de sécurité.
4. **Test** — exécute la suite de tests et produit la couverture.
5. **Build** — dans un job dédié après la réussite de `pipeline`, construit les
   distributions Python et les publie comme artefact.

Les phases Prepare à Test partagent le même runner. Le Build est isolé pour ne
pas construire ou publier un paquet si une validation précédente échoue.

## Modules

| Fichier | Responsabilité |
|---|---|
| `.github/workflows/ci.yml` | Déclencheurs, permissions minimales, annulation des runs concurrents et ordre global des jobs. |
| `.github/actions/prepare/action.yml` | Runtimes, caches et installation des dépendances Python et PHP. |
| `.github/actions/validate/action.yml` | Conventions des PR, cohérence des dépendances et rapport des mises à jour disponibles. Branche et titre sont vérifiés dans la même étape afin de partager l’échappement et d’afficher les deux erreurs si nécessaire. |
| `.github/actions/code-quality/action.yml` | Formatage, lint, analyse de types et scans de sécurité Python/PHP. |
| `.github/actions/test/action.yml` | Tests pytest, couverture et upload du rapport. |
| `.github/actions/build/action.yml` | Build du package Python et upload des distributions. |
| `.github/scripts/workflow-utils.sh` | Fonctions shell partagées par les étapes de validation, notamment l’échappement sûr des valeurs affichées dans les annotations GitHub Actions. |

## Outils utilisés

### Préparation et dépendances

| Outil | Commande/configuration | Fonction et résultat |
|---|---|---|
| `actions/checkout` | `actions/checkout@v4` | Récupère le code dans le runner. |
| `actions/setup-python` | Python `3.13`, cache `pip` | Installe Python et conserve le cache de paquets. La clé tient compte de `requirements.txt` et `pyproject.toml`. |
| `shivammathur/setup-php` | PHP `8.5`, Composer `v2` | Installe le runtime pour le parseur PHP et ses outils. |
| Cache Composer | `~/.composer/cache/files` | Réutilise les archives Composer. La clé est dérivée de `php-parser/composer.json` et `php-parser/composer.lock`. |
| `pip` | `python -m pip install -r requirements.txt -e .` | Installe les outils Python et le package AskCode en mode éditable. |
| Composer | `composer install --working-dir=php-parser --no-interaction --prefer-dist` | Installe les versions verrouillées dans `php-parser/composer.lock`, y compris PHP CS Fixer et PHPStan. |

Les caches évitent principalement le téléchargement répété des paquets. Ils ne
remplacent pas la commande d’installation et ne partagent pas un environnement
virtuel entre jobs.

### Validation des PR et dépendances

| Outil/contrôle | Règle ou commande | Échec / sortie |
|---|---|---|
| Validation de branche | `(feat\|fix\|docs\|chore\|ci)/[A-Z]+-[0-9]+-kebab-case` | Bloque une PR si le préfixe, la clé de ticket majuscule ou la description kebab-case ne correspond pas. Exemple : `feat/IT-02-add-ci`. |
| Titre Conventional Commit | `feat`, `fix`, `docs`, `chore`, `ci`, `refactor`, `test`, `build`, `perf`; scope facultatif | Bloque une PR si le titre ne ressemble pas à `feat: add CI` ou `fix(parser): handle empty input`. |
| Métadonnées de PR | Branche source et titre | Affiche les deux valeurs reçues dans le log avant les contrôles. En cas d’échec, l’annotation donne aussi la valeur concernée et le format attendu. |
| `pip check` | `python -m pip check` | Échoue si les dépendances Python installées sont incompatibles. |
| `composer validate` | `composer validate --working-dir=php-parser --no-check-publish` | Vérifie la cohérence du manifeste Composer et du lock file. |
| `pip list --outdated` | `python -m pip list --outdated` | Informe des versions Python plus récentes. `continue-on-error: true` : informatif, ne bloque pas la CI. |
| `composer outdated` | `composer outdated --working-dir=php-parser --direct` | Informe des mises à jour des dépendances PHP directes. Ne bloque pas la CI. |

La validation de branche et de titre s’applique seulement aux événements
`pull_request`; les contrôles de dépendances s’exécutent aussi sur les `push`.

### Qualité Python et PHP

| Outil | Commande/configuration | Ce qu’il contrôle |
|---|---|---|
| Ruff format | `ruff format --check src/ tests/ scripts/` | Vérifie le formatage Python sans modifier les fichiers. |
| Ruff check | `ruff check src/ tests/ scripts/` | Lint Python. Les règles `E` (style Pycodestyle) et `F` (erreurs Pyflakes) sont configurées dans `pyproject.toml`. |
| mypy | `mypy src/askcode/` | Analyse statiquement les types du package; `check_untyped_defs` est activé dans `pyproject.toml`. |
| Bandit | `bandit -r src/ scripts/ -ll -f json -o bandit-report.json` | Recherche les problèmes de sécurité Python de sévérité moyenne ou haute; écrit un rapport JSON. |
| pip-audit | `pip-audit -r requirements.txt --format json --output pip-audit-report.json` | Compare les dépendances Python déclarées aux avis de vulnérabilité connus. |
| PHP CS Fixer | `vendor/bin/php-cs-fixer fix --dry-run --diff --config=.php-cs-fixer.dist.php` depuis `php-parser/` | Vérifie le style PSR-12 sans corriger automatiquement les fichiers. |
| PHPStan | `php-parser/vendor/bin/phpstan analyse --configuration=php-parser/phpstan.neon --no-progress` | Analyse statiquement `analyze.php` au niveau 6. La configuration se trouve dans `php-parser/phpstan.neon`. |

Les rapports Bandit et pip-audit sont téléversés comme artefact `security-reports`,
y compris lorsqu’un contrôle ultérieur échoue (`if: always()`). L’absence d’un
rapport est tolérée si l’outil échoue avant de l’écrire.

### Tests, couverture et build

| Outil | Commande | Fonction et artefact |
|---|---|---|
| pytest-cov | `pytest --cov=askcode --cov-report=term-missing --cov-report=xml` | Exécute les tests et affiche la couverture dans le log. Produit `coverage.xml`, publié comme artefact `coverage-report`. |
| Python Build | `python -m build` | Construit l’archive source (`.tar.gz`) et le wheel (`.whl`) du package. |
| `actions/upload-artifact` | `coverage-report`, `security-reports`, `python-package` | Rend les rapports et distributions téléchargeables depuis le run GitHub Actions. |

## Dépendances et fichiers de configuration

- `requirements.txt` liste les outils Python de développement et de CI.
- `pyproject.toml` configure le build Python, la découverte du package, pytest,
  Ruff et mypy.
- `php-parser/composer.json` déclare PHP, `nikic/php-parser`, PHP CS Fixer et
  PHPStan.
- `php-parser/composer.lock` verrouille les versions Composer installées en CI.
- `php-parser/.php-cs-fixer.dist.php` configure PSR-12 et exclut `vendor`.
- `php-parser/phpstan.neon` configure le niveau et la cible PHPStan.

La CI ne configure pas actuellement de détection de copier-coller,
d’« assumption-to-assertions », Psalm, PHP Mess Detector, ni de tests unitaires
PHP séparés. Les tests existants sont exécutés avec pytest; le parseur PHP est
exercé par ces tests.
