# Ricerca: Workflow Ibrido VM + Locale per Miracollo

**Data**: 11 Gennaio 2026
**Ricercatrice**: Cervella Researcher
**Contesto**: Miracollo vive su VM (miracollo-cervella), vogliamo sviluppare nuove feature in locale

---

## Executive Summary

**Scenario attuale:**
- Miracollo in PRODUZIONE su VM `miracollo-cervella`
- Fix urgenti → direttamente su VM
- Nuove feature → vorremmo svilupparle in LOCALE con worktrees

**Soluzione consigliata:**
- **Git worktrees** per sviluppo locale parallelo
- **Post-receive hooks** per sync automatico VM (opzionale)
- **Branch strategy**: `main` (VM) + `feature/*` (locale) + `staging` (test pre-merge)

**TL;DR:**
- ✅ Fattibile con setup iniziale (1-2 ore)
- ⚠️ Richiede disciplina rigida su quale ambiente toccare
- 🎯 Beneficio: sviluppo feature isolato senza toccare produzione

---

## 1. Git Worktrees - Come Funzionano

### Concetto Base

Git worktree permette di avere **multiple working directories** dello stesso repo, ognuna con un branch diverso checked out contemporaneamente.

```
miracollogeminifocus/         # Main worktree (main branch)
├── .git/                     # Repository principale
├── src/
└── ...

miracollogeminifocus-worktrees/
├── feature-analytics/        # Worktree 1 (feature/analytics)
│   └── src/
├── feature-export/           # Worktree 2 (feature/export)
│   └── src/
└── hotfix-auth/              # Worktree 3 (hotfix/auth-bug)
    └── src/
```

### Vantaggi Chiave

1. **No context switching**: Non serve più `git checkout` → no perdita di lavoro in corso
2. **Shared .git**: Tutti i worktrees condividono stesso repository → un solo `git fetch` aggiorna tutti
3. **Parallel testing**: Testa feature A mentre sviluppi feature B
4. **Clean separation**: Main worktree resta pulito, esperimenti in worktrees dedicati

### Comandi Base

```bash
# Creare worktree per nuova feature (locale)
git worktree add -b feature/analytics ../miracollo-worktrees/analytics

# Creare worktree trackando branch remoto (da VM)
git worktree add -t ../miracollo-worktrees/staging origin/staging

# Vedere tutti i worktrees
git worktree list

# Rimuovere worktree
git worktree remove ../miracollo-worktrees/analytics
```

---

## 2. Branch Strategy per VM + Locale

### Schema Proposto

```
main (VM - PRODUZIONE)
  ↑
  └── staging (VM - PRE-DEPLOY)
        ↑
        └── feature/analytics (LOCALE)
        └── feature/export (LOCALE)
        └── feature/llm-integration (LOCALE)

hotfix/* (VM - FIX URGENTI)
  ↑
  └→ main (merge diretto)
```

### Regole d'Oro

| Branch | Dove | Chi lo tocca | Quando |
|--------|------|--------------|--------|
| `main` | VM | Solo merge da staging/hotfix | Deploy produzione |
| `staging` | VM | Merge da feature/* | Test pre-deploy |
| `feature/*` | LOCALE | Sviluppo quotidiano | Nuove funzionalità |
| `hotfix/*` | VM | Fix urgenti in produzione | Bug critici |

### Workflow Step-by-Step

#### Sviluppo Nuova Feature (LOCALE)

```bash
# 1. Creare worktree locale
cd ~/Developer/miracollogeminifocus
git worktree add -b feature/analytics ../miracollo-worktrees/analytics

# 2. Sviluppare
cd ../miracollo-worktrees/analytics
# ... lavoro ...
git commit -am "Feat: Add competitor analytics"

# 3. Push a origin
git push origin feature/analytics

# 4. Quando pronta → merge request su staging
# (da fare sulla VM o via GitHub/GitLab PR)
```

#### Test su Staging (VM)

```bash
# Sulla VM
cd /var/www/miracollo
git fetch origin
git checkout staging
git merge origin/feature/analytics
npm run build
# Test...
# Se OK → merge su main
```

#### Deploy a Produzione (VM)

```bash
# Sulla VM
git checkout main
git merge staging
npm run build
pm2 restart miracollo
```

#### Hotfix Urgente (VM)

```bash
# Sulla VM (bypass staging)
git checkout -b hotfix/auth-session-leak main
# ... fix ...
git commit -am "Fix: Session leak in auth"
git checkout main
git merge hotfix/auth-session-leak
git push origin main
git branch -d hotfix/auth-session-leak
```

---

## 3. Sync Automatico: Locale → VM

### Opzione A: Post-Receive Hook (Automatico)

Setup su VM per auto-deploy quando fai push.

**1. Creare bare repository sulla VM**

```bash
# Sulla VM
mkdir -p ~/git/miracollo.git
cd ~/git/miracollo.git
git init --bare
```

**2. Aggiungere post-receive hook**

```bash
# Sulla VM: ~/git/miracollo.git/hooks/post-receive
#!/bin/bash

WORK_TREE="/var/www/miracollo"
GIT_DIR="$HOME/git/miracollo.git"

# Quando ricevi push su staging → deploy
while read oldrev newrev ref
do
  if [[ $ref = refs/heads/staging ]]; then
    echo "Deploy to staging..."
    git --work-tree=$WORK_TREE --git-dir=$GIT_DIR checkout -f staging
    cd $WORK_TREE
    npm install
    npm run build
    pm2 restart miracollo-staging
    echo "Staging deployed!"
  elif [[ $ref = refs/heads/main ]]; then
    echo "Deploy to production..."
    git --work-tree=$WORK_TREE --git-dir=$GIT_DIR checkout -f main
    cd $WORK_TREE
    npm install
    npm run build
    pm2 restart miracollo
    echo "Production deployed!"
  fi
done
```

```bash
chmod +x ~/git/miracollo.git/hooks/post-receive
```

**3. Aggiungere remote locale**

```bash
# Locale
cd ~/Developer/miracollogeminifocus
git remote add vm-deploy ssh://user@miracollo-cervella:~/git/miracollo.git

# Push trigger deploy
git push vm-deploy staging  # Auto-deploy su staging
git push vm-deploy main     # Auto-deploy su produzione
```

### Opzione B: Manual Pull (Più Sicuro)

```bash
# Locale: push normalmente
git push origin feature/analytics

# VM: pull manuale
ssh miracollo-cervella
cd /var/www/miracollo
git fetch origin
git checkout staging
git merge origin/feature/analytics
npm run build
pm2 restart miracollo-staging
```

**Pro/Contro:**

| | Post-Receive Hook | Manual Pull |
|---|---|---|
| **Pro** | Automatico, veloce | Controllo totale, sicuro |
| **Contro** | Rischio deploy inatteso | Richiede accesso SSH ogni volta |
| **Quando** | Team piccolo, disciplinato | Produzione critica, zero rischi |

---

## 4. Rischi e Mitigazioni

### Rischio 1: Merge Conflicts

**Causa:** Feature branches lunghe divergono da main.

**Mitigazione:**
- ✅ Merge `main` → `feature/*` frequentemente (almeno settimanale)
- ✅ Feature branches vivono MAX 1 settimana
- ✅ Usare `git rebase main` prima di merge su staging

```bash
# Locale: tenere feature aggiornata
cd ~/miracollo-worktrees/analytics
git fetch origin
git rebase origin/main  # Rebase invece di merge → storia lineare
```

### Rischio 2: Push Accidentale su Main da Locale

**Causa:** Confusione su quale branch pushare.

**Mitigazione:**
- ✅ **Branch protection rules** su GitHub/GitLab (main/staging SOLO merge via PR)
- ✅ Git hook pre-push locale:

```bash
# .git/hooks/pre-push (locale)
#!/bin/bash
protected_branches='main staging'
current_branch=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')

for branch in $protected_branches; do
  if [ $branch = $current_branch ]; then
    echo "❌ Cannot push directly to $branch! Use PR."
    exit 1
  fi
done
```

### Rischio 3: Codice Non Testato su Staging Va in Produzione

**Causa:** Merge diretto `feature/*` → `main`.

**Mitigazione:**
- ✅ **Staging obbligatorio**: SEMPRE `feature/*` → `staging` → test → `main`
- ✅ CI/CD checks su staging (test automatici prima di permettere merge su main)
- ✅ Checklist manuale:

```markdown
## Pre-Deploy Checklist
- [ ] Feature testata in locale
- [ ] Merged su staging
- [ ] Test E2E su staging passati
- [ ] No errori in logs staging (24h)
- [ ] Approvazione team
- [ ] Merge su main
```

### Rischio 4: Dati VM vs Locale Non Sincronizzati

**Causa:** Database/file locali diversi da produzione.

**Mitigazione:**
- ✅ `.env.local` con connessione a DB di sviluppo separato
- ✅ Script per dump anonimizzato da produzione a locale:

```bash
# Sulla VM
pg_dump miracollo_prod | gzip > /tmp/backup.sql.gz
# Anonimizza dati sensibili
# scp a locale

# Locale
gunzip < backup.sql.gz | psql miracollo_dev
```

### Rischio 5: Worktree Non Traccia Remote Correttamente

**Causa:** Worktree creato senza `-t` flag → upstream non configurato.

**Mitigazione:**
- ✅ Sempre usare `-t` quando crei da remote branch:
```bash
git worktree add -t ../worktree-name origin/branch-name
```
- ✅ Configurare upstream manualmente se dimenticato:
```bash
git branch --set-upstream-to=origin/feature/analytics
```

### Rischio 6: Falsa Sicurezza - "Branch = Sicuro"

**Causa:** Pensare che lavorare su branch elimini tutti i rischi.

**Mitigazione:**
- ✅ **Code review** obbligatorio per ogni merge
- ✅ **Automated tests** in CI/CD
- ✅ **Small batches**: feature branches vivono max 3-5 giorni
- ✅ **Trunk-based mentality**: integrare spesso, piccoli cambiamenti

---

## 5. Workflow Proposto (Step-by-Step)

### Setup Iniziale (Una Volta)

**1. Struttura directory locale**

```bash
mkdir -p ~/Developer/miracollo-worktrees
cd ~/Developer/miracollogeminifocus

# Branch protection (opzionale se no GitHub/GitLab)
# Installare pre-push hook (vedi Rischio 2)
```

**2. Setup VM** (se usi post-receive hook)

```bash
ssh miracollo-cervella
mkdir -p ~/git/miracollo.git
cd ~/git/miracollo.git
git init --bare
# Copiare post-receive hook (vedi sezione 3)

# Aggiungere remote locale
exit
cd ~/Developer/miracollogeminifocus
git remote add vm ssh://user@miracollo-cervella:~/git/miracollo.git
```

**3. Creare branch staging**

```bash
# Locale
git checkout -b staging main
git push origin staging

# VM
ssh miracollo-cervella
cd /var/www/miracollo
git fetch origin
git checkout staging
```

### Sviluppo Feature (Quotidiano)

**Giorno 1: Inizio feature**

```bash
# Locale
cd ~/Developer/miracollogeminifocus
git worktree add -b feature/analytics ../miracollo-worktrees/analytics
cd ../miracollo-worktrees/analytics

# Sviluppo...
git add .
git commit -m "Feat: Add analytics dashboard structure"
git push origin feature/analytics
```

**Giorno 2-4: Iterazione**

```bash
cd ~/miracollo-worktrees/analytics

# Aggiorna con main (importante!)
git fetch origin
git rebase origin/main

# Continua sviluppo...
git commit -am "Feat: Add competitor tracking"
git push origin feature/analytics --force-with-lease  # Dopo rebase
```

**Giorno 5: Feature completa**

```bash
# Locale: Verifica finale
npm run test
npm run build

# Push finale
git push origin feature/analytics

# Merge su staging (via PR o manuale)
# Se PR su GitHub/GitLab → crea PR
# Se manuale:
ssh miracollo-cervella
cd /var/www/miracollo
git fetch origin
git checkout staging
git merge origin/feature/analytics --no-ff  # Preserva storia
npm install
npm run build
npm run test
pm2 restart miracollo-staging
```

**Test su staging (1-2 giorni)**

```bash
# Monitorare logs
ssh miracollo-cervella
pm2 logs miracollo-staging

# Se bug → fix direttamente su feature branch (locale)
cd ~/miracollo-worktrees/analytics
# fix...
git commit -am "Fix: Analytics query optimization"
git push origin feature/analytics

# Aggiorna staging
ssh miracollo-cervella
cd /var/www/miracollo
git checkout staging
git merge origin/feature/analytics
pm2 restart miracollo-staging
```

**Deploy produzione**

```bash
# Staging OK → merge su main
ssh miracollo-cervella
cd /var/www/miracollo
git checkout main
git merge staging --no-ff -m "Release: Analytics Dashboard v1.0"
git push origin main
npm install
npm run build
pm2 restart miracollo

# Cleanup worktree locale
cd ~/Developer/miracollogeminifocus
git worktree remove ../miracollo-worktrees/analytics
git branch -d feature/analytics  # Se merged
```

### Hotfix Urgente (VM Only)

```bash
# Tutto sulla VM
ssh miracollo-cervella
cd /var/www/miracollo
git checkout -b hotfix/session-leak main

# Fix rapido
vim src/auth/session.ts
git commit -am "Fix: Session leak on logout"

# Test minimale
npm run build
npm run test:unit

# Merge diretto su main
git checkout main
git merge hotfix/session-leak --no-ff
git push origin main
pm2 restart miracollo

# Merge anche su staging per allineamento
git checkout staging
git merge main
git push origin staging

# Cleanup
git branch -d hotfix/session-leak
```

---

## 6. Checklist Sicurezza

### Pre-Setup

- [ ] Backup completo VM prima di cambiare workflow
- [ ] Documentare stato attuale (`git status`, `git log`, ambiente)
- [ ] Branch protection rules configurati (se su GitHub/GitLab)
- [ ] Team allineato su nuovo workflow

### Durante Sviluppo

- [ ] Feature branch creato da `main` aggiornato
- [ ] Nome branch descrittivo (`feature/cosa-fa`, non `fix`, `test`)
- [ ] Commit frequenti con messaggi chiari
- [ ] Rebase con `main` almeno ogni 2 giorni
- [ ] Test locali passano PRIMA di push

### Pre-Merge Staging

- [ ] `npm run test` passa in locale
- [ ] `npm run build` completa senza errori
- [ ] Code review (se team)
- [ ] Feature branch aggiornata con `main` (rebase)
- [ ] Commit message segue convention (`Feat:`, `Fix:`, etc)

### Pre-Deploy Produzione

- [ ] Feature testata su staging per MIN 24 ore
- [ ] Zero errori critici in logs staging
- [ ] Test E2E passati
- [ ] Database migrations testate (se applicabile)
- [ ] Rollback plan definito
- [ ] Team notificato del deploy

### Post-Deploy

- [ ] Monitor logs produzione per 30 minuti
- [ ] Test smoke manuale su funzionalità critiche
- [ ] Metriche (errori, performance) sotto controllo
- [ ] Feature flag disabilitato se problemi (se applicabile)
- [ ] Tag release creato (`git tag v1.2.0`)

---

## 7. Best Practices

### 1. Worktree Organization

```bash
# Struttura consigliata
~/Developer/
├── miracollogeminifocus/          # Main repo
│   └── .git/
└── miracollo-worktrees/           # Tutti i worktrees
    ├── analytics/                  # feature/analytics
    ├── export/                     # feature/export
    └── llm-integration/            # feature/llm-integration
```

**Perché:** Separazione chiara, facile individuare progetti attivi.

### 2. Branch Naming Convention

```
feature/descrizione-breve    # Nuove funzionalità
fix/descrizione-bug          # Bug non critici
hotfix/descrizione-urgente   # Bug produzione critici
chore/descrizione-task       # Refactoring, dependencies
docs/descrizione-doc         # Solo documentazione
```

### 3. Commit Message Convention

```
Feat: Add competitor analytics dashboard
Fix: Resolve session timeout issue
Chore: Update dependencies to latest
Docs: Add API documentation for analytics
Refactor: Simplify auth middleware
```

**Format:** `Type: Description` (max 72 caratteri)

### 4. Rebase vs Merge

**Usare Rebase quando:**
- Aggiornare feature branch con `main`
- Storia lineare più leggibile
- Feature branch personale (non condiviso)

```bash
git fetch origin
git rebase origin/main
```

**Usare Merge quando:**
- Merge su `staging` o `main`
- Preservare storia completa
- Branch condiviso da più persone

```bash
git merge origin/feature/analytics --no-ff
```

### 5. Small Batches

**Regola:** Feature branch vive MAX 5 giorni lavorativi.

**Perché:**
- Meno rischio merge conflicts
- Feedback più rapido
- Easier to review
- Deploy frequenti = meno rischi

**Come:** Spezza feature grosse in incrementi piccoli deployabili.

### 6. Continuous Integration

Anche se small team, setup minimo CI:

```yaml
# .github/workflows/test.yml (se GitHub)
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: npm install
      - run: npm run test
      - run: npm run build
```

---

## 8. Tools Utili

### Git Aliases (Velocizzano workflow)

```bash
# ~/.gitconfig
[alias]
  # Worktree shortcuts
  wt = worktree
  wta = worktree add
  wtl = worktree list
  wtr = worktree remove

  # Branch management
  br = branch
  co = checkout
  cob = checkout -b

  # Status & Log
  st = status -sb
  lg = log --oneline --graph --decorate --all

  # Sync con main
  sync = !git fetch origin && git rebase origin/main

  # Cleanup merged branches
  cleanup = !git branch --merged | grep -v '\\*\\|main\\|staging' | xargs -n 1 git branch -d
```

**Usage:**

```bash
git wta -b feature/analytics ../miracollo-worktrees/analytics
git sync
git cleanup
```

### VS Code Worktree Support

VS Code ha supporto nativo (da luglio 2025):

- Apri worktree come workspace separato
- Git operations funzionano per worktree specifico
- Extensions condivise tra worktrees

### CLI Tool: worktree-env-sync

Per progetti con `.env` files:

```bash
npm install -g worktree-env-sync

# Sync .env tra worktrees
wt-env-sync --template .env.template --worktrees ../miracollo-worktrees/*
```

---

## 9. Confronto con Alternative

### Opzione 1: Solo VM (Stato Attuale)

**Pro:**
- Semplice
- Zero sync issues
- Un solo environment

**Contro:**
- ❌ Sviluppo lento (SSH, latency)
- ❌ Rischio toccare produzione per sbaglio
- ❌ Testing difficile senza duplicare VM

### Opzione 2: Git Worktrees + VM (CONSIGLIATO)

**Pro:**
- ✅ Sviluppo locale veloce
- ✅ Isolamento feature
- ✅ Produzione intatta
- ✅ Parallel development

**Contro:**
- ⚠️ Setup iniziale (1-2 ore)
- ⚠️ Richiede disciplina branch strategy

### Opzione 3: Tutto Locale + Deploy Script

**Pro:**
- Sviluppo locale
- Controllo totale

**Contro:**
- ❌ Nessun ambiente staging
- ❌ Deploy più rischioso (no test pre-prod)
- ❌ Richiede script deployment custom

### Opzione 4: Docker Compose Locale

**Pro:**
- Replica produzione esatta
- Isolation completo

**Contro:**
- ❌ Overhead configurazione significativo
- ❌ Risorse macchina locale
- ❌ Complexity per progetto esistente

**Verdict:** Opzione 2 (Worktrees + VM) offre miglior bilanciamento velocità/sicurezza per Miracollo.

---

## 10. Raccomandazione Finale

### TL;DR

**SÌ, adottare workflow ibrido con:**

1. **Git worktrees** per sviluppo locale feature nuove
2. **Branch strategy**: `main` (prod VM) ← `staging` (test VM) ← `feature/*` (locale)
3. **Manual pull** su VM (più sicuro che auto-deploy per ora)
4. **VM-only** per hotfix urgenti

### Implementazione Suggerita (Phased)

**Fase 1 (Settimana 1): Setup Base**
- Creare branch `staging` su VM
- Setup worktree directory locale
- Testare workflow con 1 feature piccola
- Documentare processo team

**Fase 2 (Settimana 2-3): Refinement**
- Branch protection rules (se GitHub/GitLab)
- Git hooks (pre-push locale)
- CI/CD basic (test automatici)
- Checklist template

**Fase 3 (Settimana 4+): Automation** (opzionale)
- Post-receive hooks VM per staging
- Automated tests più completi
- Monitoring & alerts

### Quando NON Usare Questo Workflow

- ❌ Feature richiede accesso diretto a dati produzione (fai su VM)
- ❌ Hotfix urgente (fai su VM)
- ❌ Debugging produzione (SSH su VM)
- ❌ Team > 5 persone (considera GitFlow più strutturato)

### Success Metrics (Dopo 1 Mese)

- [ ] Zero deploy accidentali su produzione
- [ ] Almeno 2 feature sviluppate con worktrees
- [ ] Tempo sviluppo feature ridotto 30%+
- [ ] Zero merge conflicts maggiori
- [ ] Team confortevole con workflow

---

## Fonti

### Git Worktrees
- [Git Official Docs - git-worktree](https://git-scm.com/docs/git-worktree)
- [Practical Guide to Git Worktree - DEV Community](https://dev.to/yankee/practical-guide-to-git-worktree-58o0)
- [Mastering Git Worktree - Medium](https://mskadu.medium.com/mastering-git-worktree-a-developers-guide-to-multiple-working-directories-c30f834f79a5)
- [Using Git Worktrees for Concurrent Development - Ken Muse](https://www.kenmuse.com/blog/using-git-worktrees-for-concurrent-development/)
- [Git Worktrees to Automate Development Environments - fsck.sh](https://fsck.sh/en/blog/git-worktree/)

### Branch Strategies
- [DevOps Branching Strategies - BMC Software](https://www.bmc.com/blogs/devops-branching-strategies/)
- [Branching Strategies for CI/CD - JetBrains TeamCity](https://www.jetbrains.com/teamcity/ci-cd-guide/concepts/branching-strategy/)
- [Best Branching Strategy for CI/CD - Devtron](https://devtron.ai/blog/best-branching-strategy-for-ci-cd/)
- [Developing and Deploying with Branches - Beanstalk Guides](http://guides.beanstalkapp.com/version-control/branching-best-practices.html)

### Git Deploy & Automation
- [How To Set Up Automatic Deployment with Git - DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-set-up-automatic-deployment-with-git-with-a-vps)
- [Simple Automated GIT Deployment using Hooks - GitHub Gist](https://gist.github.com/noelboss/3fe13927025b89757f8fb12e9066f2fa)
- [Simple Automated Deployments Using Git Push - garrido.io](https://garrido.io/notes/simple-automated-deployments-git-push/)

### Risks & Pitfalls
- [The Pitfalls of Feature Branching - CloudBees](https://www.cloudbees.com/blog/pitfalls-feature-branching)
- [Git Workflow - Atlassian Tutorial](https://www.atlassian.com/git/tutorials/comparing-workflows)
- [Feature Branching Guide - LaunchDarkly](https://launchdarkly.com/blog/dos-and-donts-of-feature-branching/)
- [On the Evilness of Feature Branching - ThinkingLabs](https://thinkinglabs.io/articles/2021/10/25/on-the-evilness-of-feature-branching-why-do-teams-use-feature-branches.html)

### Multi-Environment & Sync
- [Git Worktree Tutorial - DataCamp](https://www.datacamp.com/tutorial/git-worktree-tutorial)
- [worktree-env-sync - GitHub](https://github.com/thesunny/worktree-env-sync)
- [Working on Two Git Branches at Once - Andrew Lock](https://andrewlock.net/working-on-two-git-branches-at-once-with-git-worktree/)

---

**Fine Ricerca** - 11 Gennaio 2026

*Prossimi step suggeriti:*
1. Discutere raccomandazione con Rafa
2. Se approva → iniziare Fase 1 setup
3. Documentare first feature con worktree come case study
