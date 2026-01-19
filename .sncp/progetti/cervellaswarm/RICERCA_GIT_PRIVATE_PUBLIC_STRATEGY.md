# Ricerca: Git Strategy Private vs Public per CervellaSwarm

**Data:** 19 Gennaio 2026
**Ricercatrice:** Cervella Researcher
**Status:** ✅ Completata

---

## Situazione Attuale

```
LOCALE (851 commit)
├── .sncp/ (PRIVATO - memoria esterna)
├── NORD.md (PRIVATO - strategia)
├── roadmaps/ (PRIVATO)
├── docs/ (PUBBLICO - documentazione tecnica)
├── packages/ (PUBBLICO - codice CLI/MCP)
└── scripts/ (PUBBLICO - automation)

REMOTES:
├── cervellaswarm (PUBBLICO) - 1 solo commit "Initial public release v0.1.2"
└── cervellaswarm-archive (PRIVATO, ARCHIVIATO) - non più accessibile
```

**Problema:** Il locale ha 851 commit con file privati. Il remote pubblico ha solo 1 commit. Come gestiamo questo?

---

## Analisi Pattern Industry

### Pattern 1: Dual Remote (Private Origin + Public Mirror)

**Come funziona:**
```bash
origin → private-repo (development interno)
public → public-repo (release mirror)
```

**Chi lo usa:** Microsoft, Google (secondo ricerca)

**Pro:**
- Separazione netta private/public
- Controllo totale su cosa pubblicare
- Flessibilità: puoi scegliere quali commit sincronizzare

**Contro:**
- Richiede processo manuale di sync
- Rischio push accidentale su remote sbagliato
- Overhead cognitivo: "quale remote uso?"

**Workflow:**
1. Lavoro normale su `origin` (private)
2. Quando pronto: cherry-pick commit pubblici su branch `public-release`
3. Push branch `public-release` su remote `public`

---

### Pattern 2: De-Archive + Private-First

**Come funziona:**
```bash
De-archiviare cervellaswarm-archive
↓
origin → cervellaswarm-archive (PRIVATE, main development)
public → cervellaswarm (PUBLIC, release mirror)
```

**Pro:**
- Mantiene storia esistente (851 commit)
- Nessuna riscrittura history
- Semplice da implementare

**Contro:**
- Se GitHub impedisce de-archive → bloccati
- Nome "archive" confondente

---

### Pattern 3: Nuovo Repo Private + git-filter-repo

**Come funziona:**
```bash
1. Crea nuovo repo PRIVATE: cervellaswarm-internal
2. Push TUTTO il locale (851 commit)
3. Per release pubblica: git filter-repo rimuove file privati
4. Push su cervellaswarm (public)
```

**Chi lo usa:** Pattern standard per open-sourcing progetti esistenti

**Pro:**
- Nome chiaro: "internal" vs repo pubblico
- Storia completa preservata in private
- Public inizia "pulito"

**Contro:**
- Richiede creare nuovo repo
- git filter-repo è potente ma delicato

---

### Pattern 4: Monorepo con .gitignore (Sconsigliato)

**Come funziona:**
```bash
Aggiungi .sncp/ a .gitignore
Usa solo cervellaswarm (public)
```

**Pro:**
- Più semplice: un solo repo

**Contro:**
- ❌ .sncp/ NON è in .gitignore attualmente → già nel history!
- ❌ File privati già committati (851 commit) → visibili in history
- ❌ Richiede comunque riscrittura history per pulire
- ❌ Rischio dimenticare un file privato

**Verdetto:** NON SICURO per la nostra situazione.

---

## La Mia Raccomandazione: OPZIONE 3 (Dual Remote con Nuovo Private)

### PERCHÉ Questa Scelta

1. **Nome Chiaro:** `cervellaswarm-internal` è esplicito
2. **Separazione Netta:** Private = tutto, Public = solo release
3. **Sicurezza:** Impossibile push accidentale di file privati
4. **Flessibilità:** Possiamo pubblicare solo ciò che vogliamo
5. **Standard Industry:** È il pattern usato quando open-sourcing progetti esistenti

### COME Implementarla

#### Step 1: Crea Repo Private su GitHub

```bash
# Su GitHub web:
# - Crea nuovo repo: cervellaswarm-internal
# - Visibilità: PRIVATE
# - No README, no .gitignore (useremo quello esistente)
```

#### Step 2: Setup Dual Remote

```bash
cd /Users/rafapra/Developer/CervellaSwarm

# Rinomina remote attuale
git remote rename origin public

# Aggiungi nuovo private come origin (convenzione: origin = dove pusho sempre)
git remote add origin git@github.com:CervellaSwarm/cervellaswarm-internal.git

# Verifica
git remote -v
# origin    git@github.com:CervellaSwarm/cervellaswarm-internal.git (fetch)
# origin    git@github.com:CervellaSwarm/cervellaswarm-internal.git (push)
# public    git@github.com:CervellaSwarm/cervellaswarm.git (fetch)
# public    git@github.com:CervellaSwarm/cervellaswarm.git (push)
```

#### Step 3: Push TUTTO su Private

```bash
# Push tutti i branch e tag su origin (private)
git push origin --all
git push origin --tags

# Verifica su GitHub che tutto sia lì (851 commit)
```

#### Step 4: Proteggi .sncp/ per Futuro

```bash
# Aggiungi a .gitignore per evitare futuri commit accidentali in public
echo "" >> .gitignore
echo "# Private SNCP (memory external)" >> .gitignore
echo ".sncp/" >> .gitignore

git add .gitignore
git commit -m "gitignore: Proteggi .sncp/ da push pubblici accidentali"
git push origin main
```

**NOTA:** Questo NON rimuove .sncp/ dalla history esistente, ma previene FUTURI commit accidentali.

#### Step 5: Workflow Quotidiano

```bash
# Lavoro normale (su private)
git add .
git commit -m "Checkpoint: Sessione XYZ"
git push origin main  # ← Va su cervellaswarm-internal (PRIVATE)

# QUANDO pronto per release pubblica (es: v0.2.0)
# Vedi "Step 6: Release Pubblica" sotto
```

---

### Step 6: Release Pubblica (Quando Serve)

**QUANDO:** Solo per release ufficiali (es: v0.2.0, v0.3.0)

**PROCESSO:**

```bash
# 1. Crea branch release pulito
git checkout -b public-release-v0.2.0

# 2. Rimuovi file privati dalla HISTORY di questo branch
# IMPORTANTE: Questo NON tocca il branch main, solo questo branch temporaneo
git filter-repo --invert-paths \
  --path .sncp/ \
  --path NORD.md \
  --path roadmaps/ \
  --force

# 3. Verifica che file privati siano spariti
ls -la  # .sncp/ non dovrebbe esistere

# 4. Push su repo pubblico
git remote add public-temp git@github.com:CervellaSwarm/cervellaswarm.git
git push public-temp public-release-v0.2.0:main --force

# 5. Cleanup branch temporaneo
git checkout main
git branch -D public-release-v0.2.0
```

**NOTA:** Questo workflow crea un branch "monouso" per la release pubblica. Il branch main privato rimane intatto.

---

### Alternative Workflow Release (GitHub Actions)

Se vogliamo AUTOMATIZZARE:

```yaml
# .github/workflows/sync-public.yml
name: Sync Public Release

on:
  workflow_dispatch:  # Trigger manuale
    inputs:
      version:
        description: 'Version to release (e.g., v0.2.0)'
        required: true

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history

      - name: Setup git-filter-repo
        run: |
          pip install git-filter-repo

      - name: Create clean branch
        run: |
          git checkout -b public-release-${{ inputs.version }}
          git filter-repo --invert-paths \
            --path .sncp/ \
            --path NORD.md \
            --path roadmaps/ \
            --force

      - name: Push to public repo
        run: |
          git remote add public https://x-access-token:${{ secrets.PUBLIC_REPO_TOKEN }}@github.com/CervellaSwarm/cervellaswarm.git
          git push public public-release-${{ inputs.version }}:main --force
```

**Pro:** Click button, release automatica
**Contro:** Richiede setup GitHub Actions + token

---

## Confronto Opzioni (TL;DR)

| Opzione | Complessità | Sicurezza | Flessibilità | Manutenzione |
|---------|------------|-----------|--------------|--------------|
| **1. Dual Remote (pattern 1)** | ⭐⭐⭐ Media | ⭐⭐⭐ Alta | ⭐⭐⭐⭐ Alta | ⭐⭐⭐ Media |
| **2. De-Archive** | ⭐⭐ Bassa | ⭐⭐⭐ Alta | ⭐⭐ Media | ⭐⭐ Bassa |
| **3. Nuovo Private + filter (RACCOMANDATO)** | ⭐⭐⭐ Media | ⭐⭐⭐⭐⭐ Massima | ⭐⭐⭐⭐⭐ Massima | ⭐⭐⭐ Media |
| 4. Solo .gitignore | ⭐ Facile | ❌ INSICURO | ⭐ Bassa | ⭐⭐⭐⭐ Alta |

---

## Prossimi Step Suggeriti

### FASE 1: Setup Immediato (10 min)
```bash
# 1. Crea cervellaswarm-internal su GitHub (private)
# 2. Setup dual remote (vedi Step 2 sopra)
# 3. Push tutto su private (vedi Step 3)
# 4. Proteggi .sncp/ in .gitignore (vedi Step 4)
```

### FASE 2: Test Workflow (quando hai tempo)
```bash
# Prova il processo di release pubblica su un branch test
# Verifica che git filter-repo funzioni come atteso
```

### FASE 3: Documentazione (per la famiglia)
```bash
# Aggiorna CLAUDE.md con nuovo workflow git
# Documenta in NORD.md la strategia dual remote
```

---

## Domande Aperte per la Regina

1. **GitHub Actions:** Vuoi automatizzare le release pubbliche? (Richiede 1-2 ore setup)
2. **Archive Repo:** Vuoi eliminare `cervellaswarm-archive` o mantenerlo come backup?
3. **Timing:** Implemento subito o aspettiamo fine giornata?

---

## Fonti

### Documentazione Ufficiale
- [GitHub Docs: Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [GitHub Docs: Managing remote repositories](https://docs.github.com/en/get-started/getting-started-with-git/managing-remote-repositories)

### Articoli Tecnici
- [Managing Dual Git Remotes - Medium](https://medium.com/@Spritan/managing-dual-git-remotes-pulling-from-public-repos-pushing-to-private-ca7a80a74474)
- [How to Open Source a Private Project - OmbuLabs](https://www.ombulabs.ai/blog/open-source/open-sourcing-a-private-project.html)
- [Public vs Private Repositories Developer's Guide](https://daily.dev/blog/public-vs-private-repositories-developers-guide)

### Tool Documentation
- [git-filter-repo Tutorial - Tower](https://www.git-tower.com/learn/git/faq/git-filter-repo)
- [Remove Sensitive Files from Git History - Nimbus Intelligence](https://nimbusintelligence.com/2024/02/git-filter-repo-remove-sensitive-information-from-git-history-with/)

### GitHub Actions
- [Repo Selective Sync - GitHub Marketplace](https://github.com/marketplace/actions/repo-selective-sync)
- [Repo File Sync Action - GitHub Marketplace](https://github.com/marketplace/actions/repo-file-sync-action)

### Best Practices
- [GitHub Best Practices - Webstandards](https://webstandards.ca.gov/2023/04/19/github-best-practices/)
- [Git Best Practices - Seth Robertson](https://sethrobertson.github.io/GitBestPractices/)
- [Atlassian Git Workflows Tutorial](https://www.atlassian.com/git/tutorials/comparing-workflows)

---

**Fine Ricerca**

*Cervella Researcher - "Studiare prima di agire, sempre!" 🔬*
