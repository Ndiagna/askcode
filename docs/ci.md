# CI pipeline

The GitHub Actions workflow runs on pushes and pull requests targeting
`develop` or `master`. It is organized into reusable composite actions under
`.github/actions/` and a final package-build job.

## Pipeline phases

| Phase | Module | Purpose |
|---|---|---|
| Prepare | `.github/actions/prepare` | Configure Python 3.13, PHP 8.5 and Composer; restore pip and Composer caches; install Python and PHP dependencies once. |
| Validate | `.github/actions/validate` | On pull requests, enforce branch and title conventions; check Python/Composer dependency consistency; report outdated dependencies without blocking the pipeline. |
| Code quality | `.github/actions/code-quality` | Check Python formatting/lint/types/security and PHP formatting/static analysis; upload security reports. |
| Test | `.github/actions/test` | Run pytest with coverage and upload `coverage.xml`. |
| Build | `.github/actions/build` | Build the Python source and wheel distributions only after all pipeline phases succeed. |

The preparation, validation, quality, and test modules run in order in one
runner so the same installed dependencies and caches are reused. The build job
is separate and depends on the full pipeline job.

## Conventions

- Branches: `feat/IT-02-description`, `fix/IT-02-description`,
  `docs/IT-02-description`, `chore/IT-02-description`, or
  `ci/IT-02-description`. The ticket key is uppercase and the description is
  lowercase kebab-case.
- Pull request titles: Conventional Commit format, for example
  `feat: add CI workflow` or `fix(parser): handle empty input`.

## Tools

| Tool | Phase | What it checks |
|---|---|---|
| `pip` / `composer` | Prepare | Install the dependency sets declared in `requirements.txt` and `php-parser/composer.lock`. |
| `pip check` / `composer validate` | Validate | Detect incompatible installed Python dependencies and a Composer manifest/lock mismatch. |
| `pip list --outdated` / `composer outdated` | Validate | Report newer dependencies; informational only and does not fail the pipeline. |
| Ruff format | Code quality | Ensure Python files match the formatter's canonical layout without changing files. |
| Ruff check | Code quality | Find Python style and common static errors (configured `E` and `F` rule families). |
| mypy | Code quality | Check Python type consistency in `src/askcode/`. |
| Bandit | Code quality | Detect Python security issues of medium or higher severity in source and scripts. |
| pip-audit | Code quality | Check declared Python dependencies against known vulnerability advisories. |
| PHP CS Fixer | Code quality | Enforce PSR-12 formatting for `php-parser/` without modifying files. |
| PHPStan | Code quality | Statically analyse `php-parser/analyze.php` at level 6 without running it. |
| pytest-cov | Test | Run the Python tests and generate terminal and XML coverage reports. |
| `python -m build` | Build | Produce source and wheel distributions for the Python package. |

## Caching and artifacts

- `actions/setup-python` caches pip downloads using `requirements.txt` and
  `pyproject.toml` as cache keys.
- Composer downloads are cached using `php-parser/composer.json` and
  `php-parser/composer.lock`.
- Coverage, security reports, and Python distributions are uploaded as workflow
  artifacts.
