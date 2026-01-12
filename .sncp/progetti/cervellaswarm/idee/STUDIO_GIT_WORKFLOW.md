# STUDIO: Git Workflow per Team Piccolo (1-3 persone)

**Data:** 12 Gennaio 2026
**Status:** Ricerca Completata
**Focus:** Semplicità + Sicurezza + Prod Stability

---

## TL;DR - La Risposta

**TRUNK-BASED DEVELOPMENT** è la scelta migliore per il vostro caso.

Perché? Team piccolo + cambio frecquente + fix urgenti in prod = esigenze che TBD risolve meglio.

---

## 1. CONFRONTO TRE APPROCCI

| Aspetto | GitFlow | GitHub Flow | Trunk-Based |
|---------|---------|------------|------------|
| **Complessità** | Alta (develop, release, hotfix branches) | Media (1 feature branch) | Bassa (main solo) |
| **Team ideale** | 5+ persone | Piccoli team (3-5) | Piccolissimi (1-3) |
| **Velocità** | Lenta (merge multipli) | Media | Veloce (commit diretti) |
| **Hotfix in prod** | Branca dedicata + merge doppio | PR veloce in main | Commit diretto con tag |
| **Merge conflict** | MOLTO frequenti | Moderati | Rari |
| **Overhead ceremony** | Massimo | Minimo | Zero |

**Verdict:** Per 1-3 persone, GitFlow è OVERENGINEERING puro. GitHub Flow è ok, TBD è meglio.

---

## 2. TRUNK-BASED DEVELOPMENT - COME FUNZIONA

### Il Flusso Base
```
main (always deployable)
  ↑
  ├─ feature-x (1-2 giorni max)
  ├─ hotfix-urgent (30 min - 2h)
  └─ direct commits (quando feature è banale)
```

### Regole Semplici
1. **Tutti lavorano su main** (o su branch molto short-lived)
2. **Commit giornalieri** - Non isolatevi per giorni
3. **Piccoli cambiamenti** - Facili da revieware/revertare
4. **Feature flags** per lavori lunghi (codice in prod ma feature nascosta)
5. **Tag per versioni** - main sempre è la versione "stable"

### Vantaggi per Voi
- ✅ Zero branch management
- ✅ Merge conflict rarissimi
- ✅ Hotfix = commit + push + tag (5 minuti)
- ✅ Facile sincronizzare local e VM prod
- ✅ Semplicità assoluta

### Svantaggi
- ⚠️ Discipline richiesta (test prima di push)
- ⚠️ CI/CD essenziale (altrimenti main si rompe)
- ⚠️ Code review importante (perché tutto va direttamente in prod)

---

## 3. GESTIRE HOTFIX IN PRODUZIONE

### Scenario Tipico
```
Ore 14:30 - Bug trovato in prod
Ore 14:35 - Fermi il feature work in local
Ore 14:40 - Facciamo commit hotfix su main
Ore 14:45 - Pullo il commit sulla VM prod
Ore 14:50 - Done, il resto del team tira main aggiornato
```

### Procedura Hotfix (TBD Style)

```bash
# 1. Sync local con main
git pull origin main

# 2. Fix il bug localmente
# (edit files, test)

# 3. Commit con messaggio chiaro
git commit -m "HOTFIX: [descrizione bug]"

# 4. Push su main
git push origin main

# 5. Tag la versione
git tag -a v1.2.3 -m "Hotfix: bug description"
git push origin v1.2.3

# 6. Pull sulla VM produzione
# (ssh in prod e git pull, o script deploy)
```

### Come Sincronizzare Sempre
- ✅ Prima di ogni lavoro: `git pull origin main`
- ✅ Dopo ogni cambio: `git push origin main`
- ✅ Sulla VM: scheduled pull ogni 5 minuti O trigger da CI/CD
- ✅ Usa tags per versioni stabili (non commit direttamente in prod)

---

## 4. LA CHECKLIST PRATICA

### Prima di Ogni Session di Lavoro
```
□ git status (che ramo sono?)
□ git pull origin main (aggiornato?)
□ Nessun cambio uncommitted? (git add/commit)
```

### Durante il Lavoro
```
□ Lavoro su feature banale? → commit diretto
□ Lavoro su feature complessa? → short-lived branch (max 1-2 giorni)
□ Fatto? → git push origin [main/branchname]
□ Sembra stabile? → git tag vX.Y.Z
```

### Hotfix Urgente in Prod
```
□ Stop il lavoro attuale (stash se necessario)
□ git pull origin main
□ Fix il bug
□ Test localmente
□ git commit -m "HOTFIX: ..."
□ git push origin main
□ git tag vX.Y.Z
□ Pull sulla VM
□ Verificare che funziona
□ Resume il feature work
```

---

## 5. REGOLE ESSENZIALI PER TBD

### Discipline Obbligatoria
1. **Test PRIMA di commit** - Non spingete codice rotto
2. **Commit piccoli** - Una cosa per volta
3. **Messaggi chiari** - "Fix: [cosa]" "Feature: [cosa]" "HOTFIX: [cosa]"
4. **Code review fra voi** - Anche in team piccolo, uno guarda l'altro
5. **Un commit al giorno minimo** - Non lavorate isolati

### Come Evitare di Rompere Main
- Sviluppate sempre testando localmente
- Se incertezza → branca short-lived (4 ore max)
- Se richiesta feature flag → implementate (codice nascosto dietro flag)
- Revert veloce se qualcosa va male: `git revert [commit]`

---

## 6. SINCRONIZZAZIONE LOCAL + VM PROD

### Setup Ideale
```
Local Development (voi)
       ↓ git push
GitHub/GitLab main
       ↓ deployment (script/CI-CD)
VM Produzione
```

### Opzione 1: Deploy Script Manuale
```bash
# Sulla VM, ssh
cd /path/to/prod
git pull origin main
systemctl restart [service]
```

### Opzione 2: Deploy Script Automatico
```bash
# Cron ogni 5 minuti sulla VM
*/5 * * * * cd /path/to/prod && git pull origin main && systemctl restart [service]
```

### Opzione 3: Webhook + Deploy (Migliore)
GitHub Webhook → Script deploy → VM aggiornata automaticamente

---

## 7. RACCOMANDAZIONE FINALE

### Per il Vostro Team (1-3 persone)

**Implementare TRUNK-BASED DEVELOPMENT** con:
1. Main = unica branca stabile
2. Short-lived features se necessario (< 2 giorni)
3. Hotfix = commit diretti + tag versione
4. Sincronizzazione VM: Pull automatico ogni 5 min O webhook
5. Code review fra voi (breve: "Ok?" "ack")

### Perché?
- Semplicità: una sola branca = zero overhead
- Velocità: hotfix in 5 minuti, non in 1 ora
- Sicurezza: test before push + frequent integrations = meno sorprese
- Team piccolo: Git workflow NON è il collo di bottiglia

### Cosa NON Fare
- ❌ GitFlow (overcomplex per 3 persone)
- ❌ Long-lived branches (createrete conflitti assicurati)
- ❌ Ignorare test before push (TBD richiede disciplina)
- ❌ Lazy code review (in TBD tutti i commit vanno in prod)

---

## 8. NEXT STEPS

1. **Decidere deployment strategy**: Script manuale o webhook?
2. **Creare alias git** per i comandi frequenti
3. **Test workflow**: Fare un hotfix di prova per capire il flusso
4. **Documentare** in README: come fare hotfix, come deployare

---

## FONTI

- [Trunk Based Development official guide](https://trunkbaseddevelopment.com/)
- [Atlassian: Trunk-Based Development](https://www.atlassian.com/continuous-delivery/continuous-integration/trunk-based-development)
- [Mergify: TBD vs GitFlow comparison](https://mergify.com/blog/trunk-based-development-vs-gitflow-which-branching-model-actually-works)
- [Toptal: TBD vs Git Flow](https://www.toptal.com/software/trunk-based-development-git-flow)
- [GitHub Flow for small teams](https://hostman.com/tutorials/gitflow-vs-githubflow-vs-tbd/)
