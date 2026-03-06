# PyPI Trusted Publishing - Research Report
**Date**: 2026-02-18
**Status**: COMPLETA
**Package**: cervellaswarm-code-intelligence v0.1.0
**Fonti**: 10 consultate (docs.pypi.org, packaging.python.org, GitHub pypa, dreamnetworking, inventivehq, thelinuxcode)

---

## Sintesi

- Trusted Publishing = OIDC token exchange. Zero API tokens da gestire.
- Il package NON esiste ancora su PyPI -> usare "Pending Trusted Publisher"
- Workflow: 3 job (build -> testpypi -> pypi), dove pypi richiede approvazione manuale
- Monorepo: usare `working-directory` + `packages-dir` per isolare packages/code-intelligence/
- Pitfall #1: nome package su PyPI usa HYPHEN, modulo Python usa UNDERSCORE
- Pitfall #2: il filename del workflow su PyPI deve corrispondere ESATTAMENTE
- Pitfall #3: environment name deve corrispondere ESATTAMENTE tra GitHub e PyPI

---

## 1. Come Funziona Trusted Publishing

```
GitHub Actions workflow
  -> chiede OIDC token a GitHub (id-token: write permission)
  -> invia token a PyPI
  -> PyPI verifica: owner/repo/workflow/environment match?
  -> PyPI emette short-lived upload token (scade subito)
  -> pypa/gh-action-pypi-publish carica il package
```

Nessun segreto da storare su GitHub. Tutto federato via OIDC.

---

## 2. Setup PyPI - "Pending Trusted Publisher" (prima pubblicazione)

Poiche cervellaswarm-code-intelligence NON esiste ancora su PyPI, usare il flusso
"Pending Trusted Publisher" che crea il progetto al primo publish.

### Passaggi su pypi.org

1. Login su https://pypi.org
2. Menu account -> "Publishing" (non dentro un progetto, ma nel tuo account)
3. Sezione "Add a new pending trusted publisher"
4. Compila i campi:

```
PyPI Project Name:  cervellaswarm-code-intelligence
Owner:              rafapra3008
Repository name:    cervellaswarm
Workflow filename:  publish-code-intelligence.yml
Environment name:   pypi
```

5. Click "Add"

### Stessi passaggi su test.pypi.org

Ripeti identici su https://test.pypi.org/manage/account/publishing/ con:

```
PyPI Project Name:  cervellaswarm-code-intelligence
Owner:              rafapra3008
Repository name:    cervellaswarm
Workflow filename:  publish-code-intelligence.yml
Environment name:   testpypi
```

### Dopo il primo publish

Il "pending publisher" si converte automaticamente in "publisher normale".
Nessuna ulteriore configurazione richiesta.

---

## 3. Setup GitHub - Environments

Creare due environments su GitHub (Settings -> Environments):

### Environment "testpypi"
- Nessun approver richiesto (CI automatico)
- Branch filter: `main` + tag `ci/code-intel/*` (opzionale)

### Environment "pypi"
- Required reviewers: [rafapra3008] (approvazione manuale obbligatoria)
- Deployment branch rule: Only selected branches/tags -> `v*`
- Prevent self-review: NO (siamo solo noi)

---

## 4. Workflow GitHub Actions (COMPLETO)

File: `.github/workflows/publish-code-intelligence.yml`

```yaml
# Publish cervellaswarm-code-intelligence to PyPI
#
# Trigger: tag push matching ci/code-intel/v*
# Flow: build -> testpypi (auto) -> pypi (manual approval)
#
# Quality is not negotiable.

name: Publish cervellaswarm-code-intelligence

on:
  push:
    tags:
      - 'ci/code-intel/v[0-9]+.[0-9]+.[0-9]+'

# NEVER cancel publish in-flight!
concurrency:
  group: publish-code-intelligence-${{ github.ref }}
  cancel-in-progress: false

jobs:
  # -----------------------------------------------------------------------
  # JOB 1: Build + validate
  # -----------------------------------------------------------------------
  build:
    name: Build distribution
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          persist-credentials: false

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install build tools
        run: pip install build twine

      - name: Build wheel and sdist
        working-directory: packages/code-intelligence
        run: python -m build

      - name: Validate metadata and README rendering
        working-directory: packages/code-intelligence
        run: twine check dist/*

      - name: Store distribution artifacts
        uses: actions/upload-artifact@v4
        with:
          name: code-intelligence-dist
          path: packages/code-intelligence/dist/
          retention-days: 7

  # -----------------------------------------------------------------------
  # JOB 2: Publish to TestPyPI (automatic)
  # -----------------------------------------------------------------------
  publish-testpypi:
    name: Publish to TestPyPI
    needs: [build]
    runs-on: ubuntu-latest
    timeout-minutes: 10

    environment:
      name: testpypi
      url: https://test.pypi.org/p/cervellaswarm-code-intelligence

    permissions:
      id-token: write  # REQUIRED for trusted publishing

    steps:
      - name: Download distribution artifacts
        uses: actions/download-artifact@v4
        with:
          name: code-intelligence-dist
          path: dist/

      - name: Publish to TestPyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          repository-url: https://test.pypi.org/legacy/
          skip-existing: true
          verbose: true

  # -----------------------------------------------------------------------
  # JOB 3: Smoke test from TestPyPI
  # -----------------------------------------------------------------------
  smoke-test:
    name: Smoke test from TestPyPI
    needs: [publish-testpypi]
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - name: Wait for TestPyPI propagation
        run: sleep 30

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install from TestPyPI
        run: |
          pip install \
            --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple/ \
            cervellaswarm-code-intelligence

      - name: Verify import and CLI
        run: |
          python -c "import cervellaswarm_code_intelligence; print('OK:', cervellaswarm_code_intelligence.__version__)"
          cervella-search --help
          cervella-impact --help
          cervella-map --help

  # -----------------------------------------------------------------------
  # JOB 4: Publish to PyPI (MANUAL APPROVAL required)
  # -----------------------------------------------------------------------
  publish-pypi:
    name: Publish to PyPI
    needs: [smoke-test]
    runs-on: ubuntu-latest
    timeout-minutes: 10

    environment:
      name: pypi
      url: https://pypi.org/p/cervellaswarm-code-intelligence

    permissions:
      id-token: write   # REQUIRED for trusted publishing
      contents: write   # For GitHub Release

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Download distribution artifacts
        uses: actions/download-artifact@v4
        with:
          name: code-intelligence-dist
          path: dist/

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          verbose: true

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          tag_name: ${{ github.ref_name }}
          name: cervellaswarm-code-intelligence ${{ github.ref_name }}
          body: |
            ## cervellaswarm-code-intelligence ${{ github.ref_name }}

            **Install:**
            ```bash
            pip install cervellaswarm-code-intelligence
            ```

            **Changelog:** See [CHANGELOG.md](https://github.com/rafapra3008/cervellaswarm/blob/main/packages/code-intelligence/CHANGELOG.md)

            **Links:**
            - [PyPI package](https://pypi.org/p/cervellaswarm-code-intelligence)
            - [Documentation](https://github.com/rafapra3008/cervellaswarm/tree/main/packages/code-intelligence)
          draft: false
          prerelease: ${{ contains(github.ref_name, 'alpha') || contains(github.ref_name, 'beta') || contains(github.ref_name, 'rc') }}
```

---

## 5. Tag Convention per Monorepo

Il trigger usa tag dedicati al package:

```bash
# Tag per publish
git tag ci/code-intel/v0.1.0
git push origin ci/code-intel/v0.1.0
```

Questo evita conflitti con i tag npm (`v*`) usati dal workflow publish.yml esistente.

Alternativa (piu semplice ma con conflitti potenziali):
```
ci/code-intel/v0.1.0    <- Python package
v0.1.0                  <- npm package (gia usato)
```

Raccomandazione: prefisso dedicato `ci/code-intel/` per chiarezza nel monorepo.

---

## 6. Pre-Publish Checklist

### 6.1 Metadati pyproject.toml (GIA OK per v0.1.0)

- [x] `name = "cervellaswarm-code-intelligence"` - hyphen PyPI
- [x] `version = "0.1.0"` - semver
- [x] `description` - presente
- [x] `readme = "README.md"` - presente
- [x] `license = "Apache-2.0"` - SPDX format (PEP 639)
- [x] `license-files = ["LICENSE", "NOTICE"]` - file presenti
- [x] `requires-python = ">=3.10"` - specificato
- [x] `classifiers` - OSI approved, Development Status, Python versions
- [x] `authors = [{name = "CervellaSwarm Contributors"}]` - no email personale
- [x] `[project.urls]` - Homepage, Repository, Bug Tracker
- [x] `dependencies` - solo 3 (tree-sitter, tree-sitter-language-pack, networkx)

### 6.2 Verifica locale prima del publish

```bash
cd packages/code-intelligence

# 1. Pulisci build precedenti
rm -rf dist/ build/ *.egg-info src/*.egg-info

# 2. Build
pip install build twine
python -m build

# 3. Controlla che il wheel contenga i file giusti
python -m zipfile -l dist/*.whl

# 4. Valida metadata e README rendering
twine check dist/*

# 5. Test install in venv pulito
python -m venv /tmp/test_venv
/tmp/test_venv/bin/pip install dist/*.whl
/tmp/test_venv/bin/python -c "import cervellaswarm_code_intelligence; print('OK')"
/tmp/test_venv/bin/cervella-search --help

# 6. Test suite passa
pytest -q

# 7. Controlla __version__ esiste
grep -r "__version__" src/cervellaswarm_code_intelligence/
```

### 6.3 Verifica README rendering

PyPI usa `readme-renderer` (non GitHub Markdown). Alcune sintassi non sono supportate.

```bash
pip install readme-renderer
python -m readme_renderer packages/code-intelligence/README.md -o /tmp/readme_check.html
# Se esce senza errori = OK
```

### 6.4 Verifica classifiers validi

URL di riferimento: https://pypi.org/classifiers/

Classifiers nel pyproject.toml sono tutti standard e validi.

---

## 7. Common Pitfalls - Diagnostica Rapida

| Errore | Causa | Fix |
|--------|-------|-----|
| `invalid-publisher` | Typo nel workflow filename su PyPI | Deve essere ESATTAMENTE `publish-code-intelligence.yml` |
| `invalid-publisher` | Environment name sbagliato | `environment: name: pypi` deve matchare PyPI config |
| `403 Invalid API Token` | Nome package mismatch | PyPI usa hyphen: `cervellaswarm-code-intelligence` |
| `File already exists` | Versione gia caricata | PyPI e immutabile: incrementa versione. MAI ricaricare stessa versione |
| `Description rendering failed` | README syntax non supportata | `twine check dist/*` prima del push |
| `Non-user identities cannot create new projects` | Nome nel pyproject.toml != pending publisher | Deve matchare ESATTAMENTE |
| `invalid-token` | Token OIDC scaduto o malformato | Retry. Se persiste, verifica `id-token: write` permission |
| Wheel vuoto | `packages = [...]` sbagliato in pyproject.toml | Verifica `tool.hatch.build.targets.wheel` |
| `not-enabled` | OIDC backend disabilitato su PyPI | Rarissimo, contatta PyPI admins |

### Il pitfall piu insidioso: hyphen vs underscore

```
Nome PyPI (pyproject.toml name):    cervellaswarm-code-intelligence   <- HYPHEN
Modulo Python (directory src/):      cervellaswarm_code_intelligence   <- UNDERSCORE
Config PyPI Trusted Publisher:       cervellaswarm-code-intelligence   <- HYPHEN

pip install cervellaswarm-code-intelligence   <- HYPHEN (entrambi funzionano per pip)
import cervellaswarm_code_intelligence        <- UNDERSCORE (solo questo!)
```

PyPI normalizza i nomi (PEP 625): hyphen, underscore, dot sono equivalenti per lookup,
ma il nome CANONICO registrato deve matchare il campo `name` nel pyproject.toml.

---

## 8. Attestazioni PEP 740 (Feature 2024+)

Da `pypa/gh-action-pypi-publish@release/v1` (>= v1.11.0), le attestazioni sono
ABILITATE per default quando si usa Trusted Publishing.

Cosa fa: firma ogni wheel/sdist con Sigstore usando l'identita OIDC del workflow.
Risultato: verificabilita crittografica che il package viene da quel esatto workflow.

Non serve configurazione aggiuntiva. Se vuoi disabilitare:
```yaml
- uses: pypa/gh-action-pypi-publish@release/v1
  with:
    attestations: false
```

Raccomandazione: tenerle abilitate. E una feature di sicurezza con zero costo.

---

## 9. Monorepo: Nota Importante

Il workflow usa `working-directory: packages/code-intelligence` nel build job.
Il risultato `dist/` viene caricato come artifact e scaricato nella root `dist/`
del job di publish (dove `pypa/gh-action-pypi-publish` lo cerca per default).

Se si vuole essere espliciti (consigliato per chiarezza):
```yaml
- uses: pypa/gh-action-pypi-publish@release/v1
  with:
    packages-dir: dist/   # default, ma esplicito e meglio
```

Non esiste supporto built-in per multi-package monorepo nell'action: per ogni
package serve un workflow separato o un job separato con artifact distinto.

---

## 10. Sequenza Completa F1.4

```
1. [LOCALE] Pre-publish checklist (sezione 6.2)
2. [LOCALE] twine check dist/*
3. [PYPI] Crea Pending Trusted Publisher su test.pypi.org
4. [PYPI] Crea Pending Trusted Publisher su pypi.org
5. [GITHUB] Crea environment "testpypi" (no reviewers)
6. [GITHUB] Crea environment "pypi" (required reviewer: rafapra3008)
7. [CODE] Aggiunta __version__ a __init__.py (necessario per smoke test)
8. [CODE] Crea .github/workflows/publish-code-intelligence.yml
9. [GIT] git tag ci/code-intel/v0.1.0 && git push origin ci/code-intel/v0.1.0
10. [MONITOR] Osserva GitHub Actions: build -> testpypi (auto) -> smoke-test (auto)
11. [MANUAL] Approva il job "pypi" su GitHub Actions
12. [VERIFY] pip install cervellaswarm-code-intelligence
```

---

## Raccomandazione

Il setup e piu semplice di quanto sembri. I rischi principali sono:

1. **Typo nel workflow filename**: se su PyPI scrivi `publish-code-intelligence.yml`
   ma il file si chiama diversamente -> `invalid-publisher`. Scegli il nome,
   crea il file, configura PyPI in quell'ordine.

2. **Prima versione e immutabile**: se carichi v0.1.0 su PyPI e poi trovi un bug,
   DEVI pubblicare v0.1.1. Non puoi sovrascrivere. Usare TestPyPI prima e
   fondamentale.

3. **`__version__` in `__init__.py`**: il smoke test nel workflow fa
   `cervellaswarm_code_intelligence.__version__`. Verificare che sia presente.

Stima tempo: 45-60 min per primo setup completo (PyPI config + GitHub environments
+ workflow + tag + approvazione manuale).

---

*Report generato da Cervella Researcher - S368*
*Fonti: docs.pypi.org, packaging.python.org, github.com/pypa/gh-action-pypi-publish*
